"""Pruebas basicas del repositorio."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_manifest_existe():
    assert (ROOT / "manifest.json").exists()


def test_entradas_obligatorias_existen():
    for name in ("README.md", "INDEX.md", "llms.txt", "AI.md"):
        assert (ROOT / name).exists(), f"falta {name}"


def test_playbooks_tienen_front_matter():
    for path in (ROOT / "playbooks").glob("*.md"):
        if path.name in ("README.md", "_template.md"):
            continue
        assert path.read_text(encoding="utf-8").startswith("---"), f"{path.name} sin front-matter"


def test_schemas_validos_como_json():
    import json

    for path in (ROOT / "schemas").glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
