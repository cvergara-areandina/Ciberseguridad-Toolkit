#!/usr/bin/env python3
"""network_utils - DNS, reverse DNS y comprobacion de puertos.

---
id: TOOL-REC-002
type: tool
title: network_utils
summary: Resuelve DNS y reverse DNS y comprueba puertos TCP comunes. Requiere autorizacion de red.
tags: [dns, network, ports, recon]
network: optional
version: 1.0.0
status: stable
---
"""

from __future__ import annotations

import argparse
import json
import socket
import sys

DEFAULT_PORTS = (
    "21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,3306,3389,"
    "5432,5900,6379,8080,8443,9000,27017"
)


def dns_lookup(domain: str, record_type: str = "A") -> list:
    """Resuelve registros A, AAAA o el nombre canonico."""
    try:
        if record_type == "A":
            return sorted({info[4][0] for info in socket.getaddrinfo(domain, 0, socket.AF_INET)})
        if record_type == "AAAA":
            return sorted({info[4][0] for info in socket.getaddrinfo(domain, 0, socket.AF_INET6)})
        if record_type == "CNAME":
            return [socket.getfqdn(domain)]
        return [f"Tipo no soportado sin dnspython: {record_type}"]
    except socket.gaierror as error:
        return [f"Error: {error}"]
    except OSError as error:
        return [f"Error: {error}"]


def reverse_dns(ip: str) -> str | None:
    """Resuelve el PTR de una IP."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return None


def port_scan_quick(target: str, ports: list[int], timeout: float = 0.5) -> list:
    """Comprobacion TCP basica, secuencial y no intrusiva."""
    results = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                if sock.connect_ex((target, port)) == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "unknown"
                    results.append({"port": port, "service": service, "state": "open"})
            except OSError:
                continue
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Utilidades de red. Requiere --online porque realiza consultas externas.",
        epilog="Ejemplo: python tools/recon/network_utils.py dns ejemplo.com --online --json",
    )
    subparsers = parser.add_subparsers(dest="command")

    dns_parser = subparsers.add_parser("dns", help="Resolucion DNS")
    dns_parser.add_argument("target", help="Dominio a resolver")
    dns_parser.add_argument("--type", default="A", choices=["A", "AAAA", "CNAME"])

    rev_parser = subparsers.add_parser("reverse", help="Reverse DNS")
    rev_parser.add_argument("ip", help="Direccion IP")

    scan_parser = subparsers.add_parser("scan", help="Comprobacion de puertos TCP")
    scan_parser.add_argument("target", help="IP o hostname")
    scan_parser.add_argument("--ports", default=DEFAULT_PORTS, help="Lista separada por comas")

    for sub in (dns_parser, rev_parser, scan_parser):
        sub.add_argument("--json", action="store_true", help="Salida JSON")
        sub.add_argument("--online", action="store_true", help="Autoriza la consulta de red")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 2

    if not args.online:
        print(
            "Bloqueado: esta herramienta realiza consultas de red.\n"
            "Repite el comando con --online tras obtener autorizacion explicita.",
            file=sys.stderr,
        )
        return 2

    if args.command == "dns":
        records = dns_lookup(args.target, args.type)
        if args.json:
            print(json.dumps({"target": args.target, "type": args.type, "records": records}, indent=2))
        else:
            print(f"DNS {args.type} records for {args.target}:")
            for record in records:
                print(f"  {record}")
        return 0 if records and not records[0].startswith("Error") else 1

    if args.command == "reverse":
        hostname = reverse_dns(args.ip)
        if args.json:
            print(json.dumps({"ip": args.ip, "hostname": hostname}))
        else:
            print(f"Reverse DNS: {args.ip} -> {hostname}" if hostname else f"No PTR record for {args.ip}")
        return 0 if hostname else 1

    ports = [int(value.strip()) for value in args.ports.split(",") if value.strip()]
    results = port_scan_quick(args.target, ports)
    if args.json:
        print(json.dumps({"target": args.target, "scanned": len(ports), "open": results}, indent=2))
    else:
        print(f"Open ports: {len(results)}/{len(ports)}")
        for item in results:
            print(f"  Port {item['port']}/tcp - {item['service']}")
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
