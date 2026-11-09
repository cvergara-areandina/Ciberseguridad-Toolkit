# Indice maestro

Menu de consulta rapida. Cada entrada apunta a un recurso con descripcion de una linea.

Leyenda de red: `none` = 100% offline · `optional` = consulta externa opcional · `required` = requiere internet.

## Playbooks

| ID | Recurso | Descripcion | Red |
|---|---|---|---|
| PB-PHISH-001 | [phishing.md](playbooks/phishing.md) | Triage de correos sospechosos y extraccion de IOCs | none |
| PB-MAL-001 | `playbooks/malware.md` | Analisis estatico y dinamico de muestras | none |
| PB-OSINT-001 | `playbooks/osint.md` | Reconocimiento pasivo de dominios, IPs y personas | optional |
| PB-IR-001 | `playbooks/incident-response.md` | Contencion, erradicacion y recuperacion | none |
| PB-PII-001 | `playbooks/pii-audit.md` | Auditoria de datos sensibles en archivos | none |

## Documentacion

| ID | Recurso | Descripcion |
|---|---|---|
| DOC-CONV-001 | [docs/convenciones/ids-y-severidades.md](docs/convenciones/ids-y-severidades.md) | Convencion de IDs y escala de severidad |
| DOC-CONV-002 | [docs/convenciones/front-matter.md](docs/convenciones/front-matter.md) | Metadatos obligatorios en cada documento |
| DOC-TPL-001 | [docs/plantillas/reporte.md](docs/plantillas/reporte.md) | Plantilla de reporte de analisis |
| DOC-TPL-002 | [docs/plantillas/caso.md](docs/plantillas/caso.md) | Plantilla de ficha de caso |

## Herramientas

| ID | Recurso | Descripcion | Red |
|---|---|---|---|
| TOOL-FOR-001 | `tools/forense/hash_tools.py` | Hashes, tipo de archivo y entropia | none |
| TOOL-FOR-002 | `tools/forense/email_header_parser.py` | Parseo de cabeceras de correo | none |
| TOOL-REC-001 | `tools/recon/url_analyzer.py` | Analisis estatico de URLs | none |
| TOOL-REC-002 | `tools/recon/network_utils.py` | DNS, reverse DNS y puertos | optional |
| TOOL-IOC-001 | `tools/ioc/ioc_extractor.py` | Extraccion de IOCs de texto o archivos | none |
| TOOL-IOC-002 | `tools/ioc/threat_intel_api.py` | Consulta a VirusTotal / AbuseIPDB | required |
| TOOL-GES-001 | `tools/gestion/session_manager.py` | Gestion de sesiones de analisis | none |
| TOOL-GES-002 | `tools/gestion/security_tools.ps1` | Utilidades PowerShell de sistema | none |

## Esquemas

| ID | Recurso | Descripcion |
|---|---|---|
| SCH-001 | [schemas/manifest.schema.json](schemas/manifest.schema.json) | Contrato del manifiesto del repositorio |
| SCH-002 | [schemas/playbook.schema.json](schemas/playbook.schema.json) | Contrato del front-matter de playbooks |
| SCH-003 | [schemas/case.schema.json](schemas/case.schema.json) | Contrato de un caso (sin PII) |

---

> Este archivo se mantiene a mano. El indice para maquinas es [`manifest.json`](manifest.json).
