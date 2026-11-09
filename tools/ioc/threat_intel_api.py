#!/usr/bin/env python3
"""threat_intel_api - Consultas a VirusTotal y AbuseIPDB.

---
id: TOOL-IOC-002
type: tool
title: threat_intel_api
summary: Consulta reputacion de URLs, IPs y hashes en VirusTotal y AbuseIPDB con claves propias.
tags: [threat-intel, virustotal, abuseipdb, ioc]
network: required
version: 1.0.0
status: stable
---
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

ENV_VARS = {
    "virustotal": "VT_API_KEY",
    "abuseipdb": "ABUSEIPDB_API_KEY",
}


def api_key(service: str) -> str:
    """Lee la clave del entorno. Nunca se acepta por argumento (queda en el historial)."""
    return os.environ.get(ENV_VARS[service], "").strip()


def make_request(url: str, headers: dict | None = None) -> dict:
    """Peticion HTTPS con verificacion de certificado activa."""
    context = ssl.create_default_context()
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return {"error": f"HTTP {error.code}: {error.reason}"}
    except urllib.error.URLError as error:
        return {"error": f"Connection error: {error.reason}"}
    except (json.JSONDecodeError, OSError) as error:
        return {"error": str(error)}


def virustotal_url(url: str) -> dict:
    key = api_key("virustotal")
    if not key:
        return {"error": "VT_API_KEY no definida"}
    endpoint = f"https://www.virustotal.com/api/v3/urls/{urllib.parse.quote(url, safe='')}"
    result = make_request(endpoint, {"x-apikey": key})
    if "data" in result:
        attrs = result["data"].get("attributes", {})
        stats = attrs.get("last_analysis_stats", {})
        return {
            "url": url,
            "harmless": stats.get("harmless", 0),
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "undetected": stats.get("undetected", 0),
            "total_engines": sum(stats.values()),
            "categories": attrs.get("categories", {}),
        }
    return result


def virustotal_ip(ip: str) -> dict:
    key = api_key("virustotal")
    if not key:
        return {"error": "VT_API_KEY no definida"}
    result = make_request(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}", {"x-apikey": key})
    if "data" in result:
        attrs = result["data"].get("attributes", {})
        stats = attrs.get("last_analysis_stats", {})
        return {
            "ip": ip,
            "country": attrs.get("country", "N/A"),
            "asn": attrs.get("asn", "N/A"),
            "as_owner": attrs.get("as_owner", "N/A"),
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "total_engines": sum(stats.values()),
        }
    return result if "error" in result else {"error": "No data returned", "raw": result}


def virustotal_file_hash(file_hash: str) -> dict:
    key = api_key("virustotal")
    if not key:
        return {"error": "VT_API_KEY no definida"}
    result = make_request(f"https://www.virustotal.com/api/v3/files/{file_hash}", {"x-apikey": key})
    if "data" in result:
        attrs = result["data"].get("attributes", {})
        stats = attrs.get("last_analysis_stats", {})
        return {
            "hash": file_hash,
            "type": attrs.get("type_description", "N/A"),
            "names": attrs.get("names", [])[:5],
            "size": attrs.get("size", 0),
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "undetected": stats.get("undetected", 0),
            "total_engines": sum(stats.values()),
            "first_seen": attrs.get("first_submission_date", "N/A"),
            "last_seen": attrs.get("last_submission_date", "N/A"),
        }
    return result if "error" in result else {"error": "No data returned", "raw": result}


def abuseipdb(ip: str) -> dict:
    key = api_key("abuseipdb")
    if not key:
        return {"error": "ABUSEIPDB_API_KEY no definida"}
    endpoint = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    result = make_request(endpoint, {"Key": key, "Accept": "application/json"})
    if "data" in result:
        data = result["data"]
        return {
            "ip": data.get("ipAddress"),
            "is_public": data.get("isPublic"),
            "is_whitelisted": data.get("isWhitelisted"),
            "abuse_confidence": data.get("abuseConfidenceScore"),
            "country": data.get("countryCode"),
            "domain": data.get("domain"),
            "total_reports": data.get("totalReports"),
            "last_reported": data.get("lastReportedAt"),
        }
    return result if "error" in result else {"error": "No data", "raw": result}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consulta reputacion en servicios externos. Requiere --online y clave en variable de entorno.",
        epilog="Ejemplo: python tools/ioc/threat_intel_api.py --vt-hash <sha256> --online --json",
    )
    parser.add_argument("--vt-url", help="URL a consultar en VirusTotal")
    parser.add_argument("--vt-ip", help="IP a consultar en VirusTotal")
    parser.add_argument("--vt-hash", help="Hash a consultar en VirusTotal")
    parser.add_argument("--abuseip", help="IP a consultar en AbuseIPDB")
    parser.add_argument("--online", action="store_true", help="Autoriza el envio del indicador a terceros")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    args = parser.parse_args()

    if not args.online:
        print(
            "Bloqueado: esta consulta envia el indicador a un servicio externo.\n"
            "Repite el comando con --online tras obtener autorizacion explicita.",
            file=sys.stderr,
        )
        return 2

    if args.vt_url:
        result, source = virustotal_url(args.vt_url), "VirusTotal URL"
    elif args.vt_ip:
        result, source = virustotal_ip(args.vt_ip), "VirusTotal IP"
    elif args.vt_hash:
        result, source = virustotal_file_hash(args.vt_hash), "VirusTotal hash"
    elif args.abuseip:
        result, source = abuseipdb(args.abuseip), "AbuseIPDB"
    else:
        parser.print_help()
        return 2

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n=== {source} ===\n")
        for key, value in result.items():
            print(f"  {key}: {value}")

    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
