---
id: DOC-TOOLS-001
type: doc
title: Herramientas
summary: Catalogo de herramientas ejecutables, su dominio y su necesidad de red.
tags: [tools, index]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Herramientas

Requisitos: **Python 3.10+**. Sin dependencias externas (`pip install` no es necesario).

## Catalogo

| ID | Herramienta | Dominio | Que hace | Red |
|---|---|---|---|---|
| TOOL-FOR-001 | `forense/hash_tools.py` | Forense | Hashes, tipo real, entropia | none |
| TOOL-FOR-002 | `forense/email_header_parser.py` | Forense | Cabeceras de correo | none |
| TOOL-REC-001 | `recon/url_analyzer.py` | Recon | Analisis estatico de URLs | none |
| TOOL-REC-002 | `recon/network_utils.py` | Recon | DNS, reverse DNS, puertos | optional |
| TOOL-IOC-001 | `ioc/ioc_extractor.py` | IOC | Extraccion de indicadores y PII | none |
| TOOL-IOC-002 | `ioc/threat_intel_api.py` | IOC | VirusTotal, AbuseIPDB | required |
| TOOL-GES-001 | `gestion/session_manager.py` | Gestion | Sesiones de analisis | none |
| TOOL-GES-002 | `gestion/security_tools.ps1` | Gestion | Utilidades PowerShell | none |
| TOOL-GES-003 | `gestion/build_manifest.py` | Gestion | Genera `manifest.json` y `llms.txt` | none |
| TOOL-GES-004 | `gestion/validate_repo.py` | Gestion | Valida front-matter y manifiesto | none |

## Contrato de una herramienta

Toda herramienta debe cumplir:

1. `--help` con descripcion y ejemplo.
2. `--json` para salida parseable.
3. Offline por defecto; red solo con `--online` explicito.
4. Codigos de salida: `0` exito, `1` sin hallazgos, `2` error de uso.
5. Sin escritura fuera de `logs/` o del directorio indicado por `--out`.

## Estructura

```
tools/
├── _lib/        Codigo compartido (imports relativos)
├── forense/     Analisis de artefactos
├── recon/       Reconocimiento y URLs
├── ioc/         Indicadores y threat intel
├── gestion/     Sesiones, validacion, generacion
└── tests/       Pruebas con pytest
```

## Ejecutar

```bash
python tools/forense/hash_tools.py --file muestra.bin --json
python tools/gestion/validate_repo.py
python -m pytest tools/tests -q
```
