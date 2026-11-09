#!/usr/bin/env python3
"""Genera manifest.json y llms.txt a partir del front-matter de los documentos.

---
id: TOOL-GES-003
type: tool
title: build_manifest
summary: Regenera manifest.json y llms.txt a partir del front-matter de documentos y herramientas.
tags: [tooling, manifest, automation]
network: none
version: 1.0.0
status: stable
---

Uso:
    python tools/gestion/build_manifest.py            # escribe los archivos
    python tools/gestion/build_manifest.py --check    # solo verifica, no escribe

Solo biblioteca estandar. Sin red.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "manifest.json"
LLMS = ROOT / "llms.txt"

SCAN_PATTERNS = ("playbooks/**/*.md", "docs/**/*.md", "tools/**/*.py", "tools/**/*.ps1")
SKIP_FILES = {"README.md", "_template.md", "__init__.py"}
META_MARKERS = ("---", "# ---")


def parse_meta(path: Path) -> dict | None:
    """Extrae el bloque de metadatos YAML de un .md, .py o .ps1.

    El bloque se delimita con lineas `---` y debe contener al menos `id`.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    meta: dict = {}
    inside = False
    for raw in text.splitlines()[:120]:
        line = raw.strip().lstrip("#").strip()
        if line in META_MARKERS:
            if inside:
                break
            inside = True
            continue
        if not inside or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [
                item.strip().strip("\"'")
                for item in value[1:-1].split(",")
                if item.strip()
            ]
        else:
            meta[key] = value.strip("\"'")
    return meta if "id" in meta else None


def collect() -> list[dict]:
    resources: list[dict] = []
    seen: set[str] = set()
    for pattern in SCAN_PATTERNS:
        for path in sorted(ROOT.glob(pattern)):
            if path.name in SKIP_FILES or "tests" in path.parts:
                continue
            meta = parse_meta(path)
            if not meta:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            resources.append(
                {
                    "id": meta.get("id", ""),
                    "type": meta.get("type", ""),
                    "title": meta.get("title", ""),
                    "path": rel,
                    "summary": meta.get("summary", ""),
                    "tags": meta.get("tags", []),
                    "network": meta.get("network", "none"),
                    "version": meta.get("version", "0.0.0"),
                    "status": meta.get("status", "draft"),
                }
            )
    resources.sort(key=lambda item: item["id"])
    return resources


def build_llms(resources: list[dict]) -> str:
    title = "Ciberseguridad Toolkit"
    groups = {
        "playbook": "Playbooks",
        "doc": "Documentacion",
        "template": "Plantillas",
        "tool": "Herramientas",
    }
    lines = [
        f"# {title}",
        "",
        "> Repositorio abierto de playbooks, herramientas y esquemas para analisis de seguridad.",
        "> Todo el contenido es ejecutable offline, libre de PII y reutilizable por personas y modelos de lenguaje.",
        "",
    ]
    for kind, heading in groups.items():
        items = [r for r in resources if r["type"] == kind]
        if not items:
            continue
        lines.append(f"## {heading}")
        lines.append("")
        for r in items:
            note = r["summary"]
            if r["network"] != "none":
                note += f" (red: {r['network']})"
            lines.append(f"- [{r['title']}]({r['path']}): {note}")
        lines.append("")
    lines += [
        "## Optional",
        "",
        "- [Como consumir el repo desde una IA](AI.md): orden de lectura y reglas de operacion.",
        "- [Indice maestro](INDEX.md): menu completo para personas.",
        "- [Manifiesto estructurado](manifest.json): indice para maquinas.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="No escribir, solo comparar")
    args = parser.parse_args()

    existing = json.loads(MANIFEST.read_text(encoding="utf-8"))
    resources = collect()

    existing["resources"] = resources
    existing["generated_at"] = date.today().isoformat()
    payload = json.dumps(existing, ensure_ascii=False, indent=2) + "\n"
    llms = build_llms(resources)

    if args.check:
        current = json.loads(MANIFEST.read_text(encoding="utf-8"))
        expected = json.loads(payload)
        current.pop("generated_at", None)
        expected.pop("generated_at", None)
        ok = current == expected and LLMS.read_text(encoding="utf-8") == llms
        print("OK: manifest y llms.txt estan al dia" if ok else "DESACTUALIZADO: ejecuta build_manifest.py")
        return 0 if ok else 1

    MANIFEST.write_text(payload, encoding="utf-8")
    LLMS.write_text(llms, encoding="utf-8")
    print(f"OK: {len(resources)} recursos -> manifest.json, llms.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
