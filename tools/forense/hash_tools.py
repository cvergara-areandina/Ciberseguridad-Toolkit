#!/usr/bin/env python3
"""hash_tools - Hashes, tipo real de archivo y entropia.

---
id: TOOL-FOR-001
type: tool
title: hash_tools
summary: Calcula MD5, SHA-1 y SHA-256, detecta el tipo real por magic bytes y mide la entropia de Shannon.
tags: [hash, entropy, forensics, triage]
network: none
version: 1.0.0
status: stable
---
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys

MAGIC_MAP = {
    b"MZ": "PE (Windows executable)",
    b"\x7fELF": "ELF (Linux executable)",
    b"\x89PNG": "PNG image",
    b"\xff\xd8": "JPEG image",
    b"PK": "ZIP/DOCX/PPTX/JAR",
    b"GIF8": "GIF image",
    b"%PDF": "PDF document",
    b"Rar!": "RAR archive",
    b"\x1f\x8b": "GZIP archive",
    b"BM": "BMP image",
    b"<!DOCTYPE": "XML/HTML",
    b"\xd0\xcf\x11\xe0": "OLE2 (Old Office/MSI)",
    b"\xcf\xfa\xed\xfe": "Mach-O (macOS executable)",
    b"\xca\xfe\xba\xbe": "Mach-O universal binary",
}


def calculate_hashes(filepath: str) -> dict:
    """Calcula MD5, SHA-1 y SHA-256 de un archivo."""
    hashes = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256()}
    with open(filepath, "rb") as handle:
        while chunk := handle.read(8192):
            for digest in hashes.values():
                digest.update(chunk)
    return {name: digest.hexdigest() for name, digest in hashes.items()}


def detect_file_type(filepath: str) -> str:
    """Detecta el tipo real de archivo por magic bytes y proporcion de texto."""
    with open(filepath, "rb") as handle:
        sample = handle.read(4096)
    if not sample:
        return "Empty file"
    for signature, description in MAGIC_MAP.items():
        if sample[: len(signature)] == signature:
            return description
    if sample.startswith(b"\xef\xbb\xbf"):
        return "Text file (UTF-8 with BOM)"
    if sample.startswith((b"\xff\xfe", b"\xfe\xff")):
        return "Text file (UTF-16)"
    printable = sum(1 for byte in sample if 32 <= byte <= 126 or byte in (9, 10, 13))
    if printable / len(sample) > 0.85:
        return "Text file (or script)"
    return "Unknown binary data"


def calculate_entropy(filepath: str) -> float:
    """Entropia de Shannon (bits por byte) del archivo completo."""
    with open(filepath, "rb") as handle:
        data = handle.read()
    if not data:
        return 0.0
    frequency = [0] * 256
    for byte in data:
        frequency[byte] += 1
    entropy = 0.0
    for count in frequency:
        if count > 0:
            probability = count / len(data)
            entropy -= probability * math.log2(probability)
    return entropy


def entropy_verdict(entropy: float) -> str:
    if entropy > 7.0:
        return "high"
    if entropy > 6.5:
        return "above_average"
    return "normal"


def analyze(filepath: str) -> dict:
    """Ejecuta todos los controles y devuelve un diccionario serializable."""
    size = os.path.getsize(filepath)
    entropy = calculate_entropy(filepath)
    return {
        "file": os.path.basename(filepath),
        "size": size,
        "size_human": f"{size / 1024:.1f} KB",
        "hashes": calculate_hashes(filepath),
        "type": detect_file_type(filepath),
        "entropy": round(entropy, 4),
        "entropy_verdict": entropy_verdict(entropy),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analisis basico de archivos: hashes, tipo real y entropia.",
        epilog="Ejemplo: python tools/forense/hash_tools.py --file muestra.bin --json",
    )
    parser.add_argument("--file", required=True, help="Ruta del archivo a analizar")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: archivo no encontrado: {args.file}", file=sys.stderr)
        return 2

    result = analyze(args.file)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(f"File: {result['file']}")
    print(f"Size: {result['size']:,} bytes ({result['size_human']})")
    print("\n=== Hashes ===")
    for algorithm, value in result["hashes"].items():
        print(f"  {algorithm.upper()}: {value}")
    print("\n=== File Type ===")
    print(f"  Detected: {result['type']}")
    print("\n=== Entropy ===")
    print(f"  Shannon entropy: {result['entropy']:.4f} ({result['entropy_verdict']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
