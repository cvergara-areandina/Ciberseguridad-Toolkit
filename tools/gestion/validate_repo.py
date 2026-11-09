#!/usr/bin/env python3
"""Valida el repositorio: front-matter, IDs unicos, manifiesto y ausencia de PII.

---
id: TOOL-GES-004
type: tool
title: validate_repo
summary: Valida metadatos, IDs unicos, rutas del manifiesto y ausencia de PII publicada.
tags: [tooling, validation, quality]
network: none
version: 1.0.0
status: stable
---

Uso:
    python tools/gestion/validate_repo.py
    python tools/gestion/validate_repo.py --json

Salida: 0 sin problemas, 1 con problemas encontrados, 2 error de uso.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "manifest.json"

REQUIRED = ("id", "type", "title", "summary", "tags", "version", "status")
ID_RE = re.compile(r"^(PB|DOC|TOOL|SCH|TPL|EX)-([A-Z]+-)?\d{3}$")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ALLOWED_DOMAINS = ("example.com", "ejemplo.com", "example.org", "test.com", "dominio.tld")

PUBLISHED_DIRS = ("playbooks", "docs", "schemas", "examples", "tools")
SKIP_FILES = {"README.md", "_template.md", "__init__.py"}


def parse_meta(path: Path) -> dict | None:
    """Extrae el bloque YAML delimitado por `---` en .md, .py o .ps1."""
    text = path.read_text(encoding="utf-8", errors="replace")
    meta: dict = {}
    inside = False
    for raw in text.splitlines()[:120]:
        line = raw.strip().lstrip("#").strip()
        if line in ("---", "# ---"):
            if inside:
                break
            inside = True
            continue
        if not inside or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta if "id" in meta else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    args = parser.parse_args()

    issues: list[dict] = []
    seen_ids: dict[str, str] = {}

    for pattern in ("playbooks/**/*.md", "docs/**/*.md", "tools/**/*.py", "tools/**/*.ps1"):
        for path in sorted(ROOT.glob(pattern)):
            if "tests" in path.parts:
                continue
            rel = path.relative_to(ROOT).as_posix()
            meta = parse_meta(path)
            if meta is None:
                if path.name not in SKIP_FILES:
                    issues.append({"file": rel, "rule": "front-matter", "detail": "falta bloque de metadatos"})
                continue
            for key in REQUIRED:
                if key not in meta:
                    issues.append({"file": rel, "rule": "campo-obligatorio", "detail": f"falta '{key}'"})
            rid = meta.get("id", "")
            if rid and not ID_RE.match(rid):
                issues.append({"file": rel, "rule": "id-formato", "detail": f"'{rid}' no cumple el patron"})
            if rid in seen_ids:
                issues.append({"file": rel, "rule": "id-duplicado", "detail": f"'{rid}' ya usado en {seen_ids[rid]}"})
            elif rid:
                seen_ids[rid] = rel
            summary = meta.get("summary", "")
            if summary and not (20 <= len(summary) <= 200):
                issues.append({"file": rel, "rule": "summary-longitud", "detail": f"{len(summary)} caracteres"})

    # PII publicada
    for folder in PUBLISHED_DIRS:
        base = ROOT / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in (".md", ".json", ".py", ".yml", ".yaml"):
                continue
            rel = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in EMAIL_RE.findall(text):
                domain = match.split("@")[-1].lower()
                if not any(domain.endswith(d) for d in ALLOWED_DOMAINS):
                    issues.append({"file": rel, "rule": "pii-email", "detail": "email no permitido (posible PII)"})

    # Manifiesto
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for res in manifest.get("resources", []):
            target = ROOT / res.get("path", "")
            if not target.exists():
                issues.append({"file": "manifest.json", "rule": "ruta-inexistente", "detail": res.get("path", "")})
            if res.get("id") not in seen_ids:
                issues.append({"file": "manifest.json", "rule": "id-huerfano", "detail": res.get("id", "")})
    else:
        issues.append({"file": "manifest.json", "rule": "faltante", "detail": "no existe"})

    if args.json:
        print(json.dumps({"ok": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if not issues:
            print(f"OK: repositorio valido ({len(seen_ids)} recursos)")
        else:
            print(f"FALLOS: {len(issues)}")
            for issue in issues:
                print(f"  [{issue['rule']}] {issue['file']}: {issue['detail']}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
