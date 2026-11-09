#!/usr/bin/env python3
"""ioc_extractor - Extraccion de IOCs y datos sensibles.

---
id: TOOL-IOC-001
type: tool
title: ioc_extractor
summary: Extrae IPs, dominios, URLs, hashes y correos, y opcionalmente detecta PII enmascarada.
tags: [ioc, extraction, pii, defang, triage]
network: none
version: 1.0.0
status: stable
---
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlparse

IPV4_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")
DOMAIN_RE = re.compile(r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b")
URL_RE = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[-\w$.+!*'(),;:@&=?/~#%]*)?", re.I)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
HEX_RE = re.compile(r"\b[a-fA-F0-9]{32,64}\b")
PHONE_RE = re.compile(r"(?<![\w.])(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}(?![\w.])")
LONG_DIGITS_RE = re.compile(r"\b\d{13,19}\b")
RFC_RE = re.compile(r"\b[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}\b")
CURP_RE = re.compile(r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b")


def defang(value: str) -> str:
    """Neutraliza un indicador para compartirlo sin riesgo."""
    return (
        value.replace("https://", "hxxps://")
        .replace("http://", "hxxp://")
        .replace(".", "[.]")
        .replace("@", "[at]")
    )


def mask(value: str) -> str:
    """Enmascara un dato personal conservando solo su forma."""
    if "@" in value:
        local, _, domain = value.partition("@")
        name, _, tld = domain.rpartition(".")
        return f"{local[:1]}***@{name[:1]}***.{tld}"
    digits = re.sub(r"\D", "", value)
    if len(digits) >= 4:
        return f"***{digits[-4:]}"
    return "***"


def extract_iocs(text: str) -> dict:
    """Extrae indicadores tecnicos del texto."""
    urls = sorted(set(URL_RE.findall(text)))
    url_domains = {urlparse(url).netloc.lower() for url in urls}

    domains = sorted(
        {
            domain
            for domain in DOMAIN_RE.findall(text)
            if not re.match(r"^\d+\.\d+\.\d+\.\d+$", domain)
            and domain.lower() not in url_domains
        }
    )

    hashes = {"md5": [], "sha1": [], "sha256": []}
    for match in HEX_RE.finditer(text):
        value = match.group()
        if len(value) == 32:
            hashes["md5"].append(value)
        elif len(value) == 40:
            hashes["sha1"].append(value)
        elif len(value) == 64:
            hashes["sha256"].append(value)

    return {
        "ipv4": sorted(set(IPV4_RE.findall(text))),
        "domains": domains,
        "urls": urls,
        "emails": sorted(set(EMAIL_RE.findall(text))),
        "hashes_md5": sorted(set(hashes["md5"])),
        "hashes_sha1": sorted(set(hashes["sha1"])),
        "hashes_sha256": sorted(set(hashes["sha256"])),
    }


def extract_pii(text: str) -> dict:
    """Detecta datos personales. Devuelve valores enmascarados."""
    return {
        "emails": [mask(v) for v in sorted(set(EMAIL_RE.findall(text)))],
        "phones": [mask(v) for v in sorted(set(PHONE_RE.findall(text))) if len(re.sub(r"\D", "", v)) >= 7],
        "long_digits": [mask(v) for v in sorted(set(LONG_DIGITS_RE.findall(text)))],
        "rfc": sorted(set(RFC_RE.findall(text))),
        "curp": sorted(set(CURP_RE.findall(text))),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extrae IOCs de texto o archivos. Todo el procesamiento es local.",
        epilog="Ejemplo: python tools/ioc/ioc_extractor.py --file correo.eml --json --defang",
    )
    parser.add_argument("file", nargs="?", help="Archivo a escanear")
    parser.add_argument("--file", dest="file_opt", help="Archivo a escanear (forma recomendada)")
    parser.add_argument("--text", help="Texto en linea")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    parser.add_argument("--defang", action="store_true", help="Neutraliza dominios y URLs")
    parser.add_argument("--pii", action="store_true", help="Incluye deteccion de datos personales")
    args = parser.parse_args()

    path = args.file_opt or args.file
    if args.text:
        text = args.text
    elif path:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        return 2

    iocs = extract_iocs(text)
    if args.defang:
        iocs["urls"] = [defang(v) for v in iocs["urls"]]
        iocs["domains"] = [defang(v) for v in iocs["domains"]]
        iocs["emails"] = [defang(v) for v in iocs["emails"]]

    if args.pii:
        iocs["pii"] = extract_pii(text)

    total = sum(len(v) for key, v in iocs.items() if key != "pii")

    if args.json:
        print(json.dumps({"total": total, **iocs}, indent=2, ensure_ascii=False))
        return 0 if total else 1

    print(f"Total IOCs found: {total}")
    for category, items in iocs.items():
        if not items:
            continue
        print(f"\n  {category.replace('_', ' ').upper()} ({len(items)}):")
        if isinstance(items, dict):
            for sub, values in items.items():
                for value in values[:10]:
                    print(f"    {sub}: {value}")
        else:
            for item in items[:10]:
                print(f"    {item}")
            if len(items) > 10:
                print(f"    ... and {len(items) - 10} more")
    return 0 if total else 1


if __name__ == "__main__":
    sys.exit(main())
