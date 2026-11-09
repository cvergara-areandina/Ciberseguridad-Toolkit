#!/usr/bin/env python3
"""url_analyzer - Analisis estatico de URLs.

---
id: TOOL-REC-001
type: tool
title: url_analyzer
summary: Extrae y puntua URLs por TLD sospechoso, IP literal, acortadores, subdominios y typosquatting.
tags: [url, phishing, recon, typosquatting]
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

SUSPICIOUS_TLDS = {
    "tk", "ml", "ga", "cf", "gq", "xyz", "top", "club", "work", "bid",
    "loan", "date", "win", "mom", "men", "download", "racing", "review",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "ow.ly", "t.co", "is.gd", "buff.ly",
    "shorturl.at", "goo.gl", "tiny.cc", "tr.im", "v.gd", "cli.gs",
}

TYPO_PATTERNS = [
    ("paypal", "paypa1", "paypaI"),
    ("google", "go0gle", "g00gle"),
    ("facebook", "faceb00k", "facebo0k"),
    ("microsoft", "micr0s0ft", "micr0soft"),
    ("amazon", "arnazon", "amaz0n"),
    ("netflix", "netf1ix", "n3tflix"),
]

URL_RE = re.compile(
    r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?::\d+)?(?:/[-\w$.+!*'(),;:@&=?/~#%]*)?",
    re.IGNORECASE,
)


def defang(value: str) -> str:
    """Neutraliza un indicador para poder compartirlo sin riesgo de clic."""
    return (
        value.replace("https://", "hxxps://")
        .replace("http://", "hxxp://")
        .replace(".", "[.]")
        .replace("@", "[at]")
    )


def extract_urls(text: str) -> list:
    """Extrae URLs unicas de un texto."""
    return sorted(set(URL_RE.findall(text)))


def analyze_url(url: str) -> dict:
    """Puntua una URL segun patrones de riesgo conocidos."""
    parsed = urlparse(url)
    domain = (parsed.netloc or "").lower()
    path = parsed.path or "/"
    query = parsed.query or ""

    result = {
        "url": url,
        "protocol": parsed.scheme,
        "domain": domain,
        "port": parsed.port,
        "path": path,
        "query": query,
        "flags": [],
        "score": 0,
    }

    if re.match(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$", domain):
        result["flags"].append("IP_ADDRESS_INSTEAD_OF_DOMAIN")
        result["score"] += 3

    tld = domain.split(".")[-1].lower() if "." in domain else ""
    if tld in SUSPICIOUS_TLDS:
        result["flags"].append(f"SUSPICIOUS_TLD: .{tld}")
        result["score"] += 2

    if "@" in url:
        result["flags"].append("AUTH_INFO_IN_URL (@ symbol)")
        result["score"] += 3

    if domain in SHORTENERS:
        result["flags"].append(f"URL_SHORTENER: {domain}")
        result["score"] += 2

    if len(domain.split(".")) > 3:
        result["flags"].append(f"EXCESSIVE_SUBDOMAINS ({len(domain.split('.'))} levels)")
        result["score"] += 1

    for legitimate, *variants in TYPO_PATTERNS:
        for variant in variants:
            if variant in domain:
                result["flags"].append(f"TYPO_SQUATTING: {domain} looks like {legitimate}")
                result["score"] += 3

    if re.search(r"\.(exe|scr|bat|cmd|ps1|vbs|js|jar|hta|dll)$", path, re.I):
        result["flags"].append("SUSPICIOUS_EXTENSION in path")
        result["score"] += 2

    if query and len(query) > 50 and re.match(r"^[A-Za-z0-9+/=]+$", query):
        result["flags"].append("POSSIBLE_BASE64_IN_QUERY")
        result["score"] += 1

    if url.startswith("//"):
        result["flags"].append("PROTOCOL_RELATIVE_URL")
        result["score"] += 1

    if result["score"] >= 5:
        result["risk"] = "HIGH"
    elif result["score"] >= 2:
        result["risk"] = "MEDIUM"
    else:
        result["risk"] = "LOW"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analiza URLs en busca de patrones sospechosos. No realiza peticiones de red.",
        epilog="Ejemplo: python tools/recon/url_analyzer.py --url 'http://ejemplo.tk/login' --json",
    )
    parser.add_argument("file", nargs="?", help="Archivo con texto o URLs")
    parser.add_argument("--file", dest="file_opt", help="Archivo con texto o URLs (forma recomendada)")
    parser.add_argument("--url", help="URL unica a analizar")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    parser.add_argument("--defang", action="store_true", help="Neutraliza los indicadores en la salida")
    args = parser.parse_args()

    path = args.file_opt or args.file
    if args.url:
        urls = [args.url]
    elif path:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            urls = extract_urls(handle.read())
        if not urls:
            print("No URLs found in file")
            return 1
    elif not sys.stdin.isatty():
        urls = extract_urls(sys.stdin.read())
        if not urls:
            print("No URLs found in stdin")
            return 1
    else:
        parser.print_help()
        return 2

    results = [analyze_url(url) for url in urls]

    if args.defang:
        for item in results:
            item["url"] = defang(item["url"])
            item["domain"] = defang(item["domain"])

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    high = sum(1 for item in results if item["risk"] == "HIGH")
    medium = sum(1 for item in results if item["risk"] == "MEDIUM")
    print(f"URLs analyzed: {len(results)}")
    print(f"  High risk:   {high}")
    print(f"  Medium risk: {medium}")
    print(f"  Low risk:    {len(results) - high - medium}")
    for item in results:
        print(f"\nURL: {item['url']}")
        print(f"  Domain: {item['domain']}")
        print(f"  Risk: {item['risk']}")
        for flag in item["flags"]:
            print(f"  [!] {flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
