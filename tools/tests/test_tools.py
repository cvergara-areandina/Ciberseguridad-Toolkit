"""Pruebas de las herramientas migradas."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hash_tools_detecta_texto(tmp_path):
    target = tmp_path / "muestra.txt"
    target.write_text("contenido de prueba", encoding="utf-8")
    module = load("tools/forense/hash_tools.py")
    result = module.analyze(str(target))
    assert len(result["hashes"]["sha256"]) == 64
    assert "Text" in result["type"]
    assert result["entropy"] > 0


def test_url_analyzer_marca_typosquatting():
    module = load("tools/recon/url_analyzer.py")
    result = module.analyze_url("http://paypa1.tk/login")
    assert result["risk"] == "HIGH"
    assert any("TYPO_SQUATTING" in flag for flag in result["flags"])


def test_defang_neutraliza():
    module = load("tools/recon/url_analyzer.py")
    assert module.defang("http://ejemplo.com/a@b") == "hxxp://ejemplo[.]com/a[at]b"


def test_ioc_extractor_encuentra_indicadores():
    module = load("tools/ioc/ioc_extractor.py")
    iocs = module.extract_iocs("ip 8.8.8.8 y correo persona@ejemplo.com")
    assert "8.8.8.8" in iocs["ipv4"]
    assert "persona@ejemplo.com" in iocs["emails"]


def test_pii_enmascarada():
    module = load("tools/ioc/ioc_extractor.py")
    pii = module.extract_pii("contacto: persona@ejemplo.com")
    assert pii["emails"] == ["p***@e***.com"]


def test_email_parser_avisa_sin_autenticacion():
    module = load("tools/forense/email_header_parser.py")
    parsed = module.parse_email_headers("From: a@ejemplo.com\nTo: b@ejemplo.com\nSubject: hola\n")
    assert any("Authentication-Results" in warning for warning in parsed["warnings"])


def test_session_manager_crea_y_cierra(tmp_path):
    module = load("tools/gestion/session_manager.py")
    session = module.create_session(tmp_path, "tester", "demo", "prueba")
    assert (tmp_path / "logs" / session["session_id"] / "session.json").exists()
    assert module.save_finding(tmp_path, session["session_id"], {"title": "x", "severity": "info", "detail": "y"})
    assert module.close_session(tmp_path, session["session_id"], "ok")
    sessions = module.list_sessions(tmp_path, "completed")
    assert sessions and sessions[0]["conclusion"] == "ok"
