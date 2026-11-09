#!/usr/bin/env python3
"""session_manager - Gestion de sesiones de analisis.

---
id: TOOL-GES-001
type: tool
title: session_manager
summary: Crea, actualiza, lista y cierra sesiones de analisis con hallazgos y conclusion.
tags: [sessions, workflow, case-management]
network: none
version: 1.0.0
status: stable
---
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_ROOT = Path(os.environ.get("CYBERSEC_HOME", os.getcwd()))


def paths(root: Path) -> dict:
    logs = root / "logs"
    return {
        "logs": logs,
        "inbox": root / "inbox",
        "evidence": logs / "evidence",
    }


def generate_session_id() -> str:
    return datetime.now().strftime("session_%Y%m%d_%H%M%S")


def get_session_path(root: Path, session_id: str) -> Path:
    return paths(root)["logs"] / session_id


def create_session(root: Path, analyst: str = "", target: str = "", description: str = "") -> dict:
    session_id = generate_session_id()
    session_path = get_session_path(root, session_id)
    session_path.mkdir(parents=True, exist_ok=True)

    session_data = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "analyst": analyst or "analyst",
        "target": target,
        "description": description,
        "findings": [],
        "evidence_files": [],
        "status": "in_progress",
        "conclusion": "",
    }

    (session_path / "session.json").write_text(
        json.dumps(session_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (session_path / "analysis.md").write_text(
        f"# Analisis: {session_id}\n\n"
        f"**Fecha**: {session_data['created_at']}\n"
        f"**Analista**: {session_data['analyst']}\n"
        f"**Objetivo**: {target or 'No especificado'}\n"
        f"**Descripcion**: {description or 'N/A'}\n\n"
        "---\n\n## Hallazgos\n\n## Recomendaciones\n",
        encoding="utf-8",
    )
    return session_data


def save_finding(root: Path, session_id: str, finding: dict) -> bool:
    session_file = get_session_path(root, session_id) / "session.json"
    if not session_file.exists():
        print(f"Error: sesion no encontrada: {session_id}", file=sys.stderr)
        return False
    data = json.loads(session_file.read_text(encoding="utf-8"))
    data["findings"].append(finding)
    session_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def close_session(root: Path, session_id: str, conclusion: str = "") -> bool:
    session_file = get_session_path(root, session_id) / "session.json"
    if not session_file.exists():
        print(f"Error: sesion no encontrada: {session_id}", file=sys.stderr)
        return False
    data = json.loads(session_file.read_text(encoding="utf-8"))
    data["status"] = "completed"
    data["completed_at"] = datetime.now().isoformat(timespec="seconds")
    if conclusion:
        data["conclusion"] = conclusion
    session_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def list_sessions(root: Path, status: str | None = None) -> list:
    logs = paths(root)["logs"]
    if not logs.exists():
        return []
    sessions = []
    for item in sorted(logs.iterdir(), reverse=True):
        session_file = item / "session.json"
        if item.is_dir() and session_file.exists():
            data = json.loads(session_file.read_text(encoding="utf-8"))
            if status is None or data.get("status") == status:
                sessions.append(data)
    return sessions


def inbox_files(root: Path) -> list:
    inbox = paths(root)["inbox"]
    if not inbox.exists():
        return []
    return [
        {
            "name": item.name,
            "size": item.stat().st_size,
            "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat(timespec="seconds"),
        }
        for item in inbox.iterdir()
        if item.is_file()
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gestiona sesiones de analisis en <root>/logs. Por defecto usa el directorio actual.",
        epilog="Ejemplo: python tools/gestion/session_manager.py new --target muestra.eml --desc triage",
    )
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Directorio de trabajo (default: CYBERSEC_HOME o cwd)")
    sub = parser.add_subparsers(dest="command")

    p_new = sub.add_parser("new", help="Crea una sesion")
    p_new.add_argument("--target", help="Objetivo del analisis")
    p_new.add_argument("--desc", help="Descripcion")
    p_new.add_argument("--analyst", default="analyst", help="Nombre o seudonimo del analista")

    p_finding = sub.add_parser("finding", help="Anade un hallazgo")
    p_finding.add_argument("session", help="ID de sesion")
    p_finding.add_argument("--title", required=True, help="Titulo del hallazgo")
    p_finding.add_argument("--severity", choices=["critical", "high", "medium", "low", "info"], default="info")
    p_finding.add_argument("--detail", default="", help="Detalle")

    p_close = sub.add_parser("close", help="Cierra una sesion")
    p_close.add_argument("session", help="ID de sesion")
    p_close.add_argument("--conclusion", default="", help="Conclusion final")

    p_list = sub.add_parser("list", help="Lista sesiones")
    p_list.add_argument("--status", choices=["in_progress", "completed"])
    p_list.add_argument("--json", action="store_true", help="Salida JSON")

    p_view = sub.add_parser("view", help="Muestra una sesion")
    p_view.add_argument("session", help="ID de sesion")

    p_inbox = sub.add_parser("inbox", help="Operaciones de inbox")
    p_inbox.add_argument("action", choices=["list", "add"], nargs="?", default="list")
    p_inbox.add_argument("file", nargs="?", help="Archivo a copiar al inbox")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.command == "new":
        print(json.dumps(create_session(root, args.analyst, args.target, args.desc), indent=2, ensure_ascii=False))
        return 0

    if args.command == "finding":
        finding = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "title": args.title,
            "severity": args.severity,
            "detail": args.detail,
        }
        if not save_finding(root, args.session, finding):
            return 1
        print(f"Hallazgo guardado en: {args.session}")
        return 0

    if args.command == "close":
        if not close_session(root, args.session, args.conclusion):
            return 1
        print(f"Sesion cerrada: {args.session}")
        return 0

    if args.command == "list":
        sessions = list_sessions(root, args.status)
        if args.json:
            print(json.dumps(sessions, indent=2, ensure_ascii=False))
            return 0
        if not sessions:
            print("No hay sesiones.")
            return 1
        for session in sessions:
            print(
                f"  {session['session_id']} | {session['status']:12s} | "
                f"{session.get('target', '?')[:30]:30s} | {len(session.get('findings', []))} findings"
            )
        return 0

    if args.command == "view":
        session_file = get_session_path(root, args.session) / "session.json"
        if not session_file.exists():
            print(f"Error: sesion no encontrada: {args.session}", file=sys.stderr)
            return 1
        print(json.dumps(json.loads(session_file.read_text(encoding="utf-8")), indent=2, ensure_ascii=False))
        return 0

    if args.command == "inbox":
        if args.action == "add":
            if not args.file:
                print("Error: indica la ruta del archivo", file=sys.stderr)
                return 2
            source = Path(args.file)
            if not source.is_file():
                print(f"Error: no existe: {args.file}", file=sys.stderr)
                return 2
            destination = paths(root)["inbox"]
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination / source.name)
            print(f"Copiado a inbox: {destination / source.name}")
            return 0
        files = inbox_files(root)
        if not files:
            print("Inbox vacio.")
            return 1
        for item in files:
            print(f"  {item['name']:40s} {item['size']:>10,} bytes")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
