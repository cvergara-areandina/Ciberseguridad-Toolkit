#!/usr/bin/env python3
"""email_header_parser - Analisis de cabeceras de correo.

---
id: TOOL-FOR-002
type: tool
title: email_header_parser
summary: Parsea cabeceras de correo, extrae cadena Received y evalua SPF, DKIM y DMARC.
tags: [email, headers, phishing, spf, dkim, dmarc]
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

KEY_HEADERS = ("From", "To", "Subject", "Date", "Reply-To", "Return-Path", "Message-ID")


def parse_email_headers(raw_headers: str) -> dict:
    """Parsea cabeceras crudas a una estructura con avisos de seguridad."""
    result: dict = {"received": [], "authentication": {}, "headers": {}, "warnings": []}

    lines = raw_headers.strip().split("\n")
    current_key = None
    current_value = ""

    for line in lines:
        line = line.rstrip()
        if not line:
            break
        if ":" in line and not line.startswith((" ", "\t")):
            if current_key:
                result["headers"][current_key] = current_value.strip()
            current_key, current_value = line.split(":", 1)
            current_key = current_key.strip()
            current_value = current_value.strip()
        elif current_key:
            current_value += " " + line.strip()

    if current_key:
        result["headers"][current_key] = current_value.strip()

    auth = result["headers"].get("Authentication-Results", "")
    for match in re.finditer(r"(spf|dkim|dmarc)\s*=\s*(\w+)", auth, re.I):
        result["authentication"][match.group(1).upper()] = match.group(2).lower()

    for line in lines:
        if line.strip().lower().startswith("received:"):
            result["received"].append(line.strip())

    result["warnings"] = check_warnings(result["headers"])
    return result


def _domain(address: str) -> str:
    return address.split("@")[-1].strip().strip("<>").lower() if "@" in address else ""


def check_warnings(headers: dict) -> list:
    """Aplica comprobaciones basicas de autenticacion y coherencia."""
    warnings = []
    auth = headers.get("Authentication-Results", "").lower()

    if "spf=fail" in auth or "spf=softfail" in auth:
        warnings.append("SPF check FAILED - sender IP not authorized")
    if "spf=none" in auth:
        warnings.append("No SPF result for sender domain")
    if "dkim=fail" in auth:
        warnings.append("DKIM signature FAILED - content may be tampered")
    if "dmarc=fail" in auth:
        warnings.append("DMARC policy FAILED - domain may be spoofed")
    if not auth:
        warnings.append("No Authentication-Results header - SPF/DKIM/DMARC not verifiable")

    from_addr = headers.get("From", "")
    reply_to = headers.get("Reply-To", "")
    return_path = headers.get("Return-Path", "")

    if reply_to and from_addr and _domain(reply_to) != _domain(from_addr):
        warnings.append(
            f"Reply-To domain ({_domain(reply_to)}) differs from From domain ({_domain(from_addr)})"
        )
    if return_path and from_addr and _domain(return_path) != _domain(from_addr):
        warnings.append(
            f"Return-Path domain ({_domain(return_path)}) differs from From domain ({_domain(from_addr)})"
        )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analiza cabeceras de correo en busca de senales de phishing.",
        epilog="Ejemplo: python tools/forense/email_header_parser.py correo.eml --json",
    )
    parser.add_argument("file", nargs="?", help="Archivo con cabeceras crudas")
    parser.add_argument("--file", dest="file_opt", help="Archivo con cabeceras crudas (forma recomendada)")
    parser.add_argument("--stdin", action="store_true", help="Leer de stdin")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    args = parser.parse_args()

    path = args.file_opt or args.file
    if args.stdin or (not path and not sys.stdin.isatty()):
        content = sys.stdin.read()
    elif path:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()
    else:
        parser.print_help()
        return 2

    if not content.strip():
        print("Error: sin contenido", file=sys.stderr)
        return 2

    parsed = parse_email_headers(content)

    if args.json:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print("=== Email Header Analysis ===\n")
        print("--- Key Headers ---")
        for key in KEY_HEADERS:
            if key in parsed["headers"]:
                print(f"  {key}: {parsed['headers'][key]}")
        if parsed["authentication"]:
            print("\n--- Authentication ---")
            for method, status in parsed["authentication"].items():
                print(f"  {method}: {'OK' if status == 'pass' else 'FAIL'} ({status})")
        if parsed["received"]:
            print(f"\n--- Received Chain ({len(parsed['received'])} hops) ---")
            for hop in parsed["received"][:5]:
                print(f"  {hop[:150]}")
        if parsed["warnings"]:
            print("\n--- WARNINGS ---")
            for warning in parsed["warnings"]:
                print(f"  [!] {warning}")
        else:
            print("\n--- No warnings detected ---")

    return 1 if parsed["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())
