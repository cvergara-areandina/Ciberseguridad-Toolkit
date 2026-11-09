---
id: DOC-PB-001
type: doc
title: Playbooks
summary: Indice de procedimientos de analisis disponibles en el repositorio.
tags: [playbooks, index]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Playbooks

Procedimientos paso a paso. Cada uno declara entradas, salidas y necesidad de red.

| ID | Playbook | Cuando usarlo | Red |
|---|---|---|---|
| PB-PHISH-001 | [phishing.md](phishing.md) | Correo sospechoso | none |
| PB-MAL-001 | [malware.md](malware.md) | Muestra sospechosa | none |
| PB-OSINT-001 | [osint.md](osint.md) | Reconocimiento pasivo | optional |
| PB-IR-001 | [incident-response.md](incident-response.md) | Incidente confirmado | none |
| PB-PII-001 | [pii-audit.md](pii-audit.md) | Datos sensibles en archivos | none |

## Crear un playbook nuevo

1. Copia [`_template.md`](_template.md).
2. Asigna un ID nuevo y unico.
3. Completa el front-matter (ver `docs/convenciones/front-matter.md`).
4. Anadelo a `INDEX.md`, `llms.txt` y `manifest.json`.
5. Ejecuta `python tools/gestion/validate_repo.py`.
