# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Versionado: [SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Estructura base del repositorio Ciberseguridad Toolkit.
- Entradas para humanos (`README.md`, `INDEX.md`) y para IA (`llms.txt`, `manifest.json`, `AI.md`).
- Convenciones de IDs, severidades y front-matter.
- Plantillas de reporte y de caso.
- Playbooks iniciales: phishing, malware, OSINT, respuesta a incidentes y auditoria PII.
- Esquemas JSON: manifiesto, playbook y caso.
- Validador de repositorio y generador de manifiesto.
- Migracion de las 8 herramientas existentes a `tools/<dominio>/` con contrato comun (`--json`, `--help`, codigos 0/1/2).
- Dos herramientas nuevas: `build_manifest.py` y `validate_repo.py`.
- Bloqueo de red por defecto en `network_utils.py` y `threat_intel_api.py` (requieren `--online`).
- Soporte `--defang` y `--pii` en `ioc_extractor.py`.

### Security

- `threat_intel_api.py`: se elimino la desactivacion de verificacion TLS (`CERT_NONE`).
- `security_tools.ps1`: se corrigieron entidades HTML (`&lt;`, `&gt;`) que rompian el script.
- `hash_tools.py`: deteccion de tipo corregida para archivos de texto con BOM.

### Pending

- Definicion de licencias (codigo y documentacion).
- Flujo de CI verificado en remoto.

## [0.1.0] - 2026-11-09

- Esqueleto inicial.
