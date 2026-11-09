---
id: TPL-002
type: template
title: Plantilla de ficha de caso
summary: Registro minimo de un caso alineado al esquema case.schema.json.
tags: [template, case]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Ficha de caso

```json
{
  "id": "CASE-2026-001",
  "title": "Titulo descriptivo sin datos personales",
  "playbook": "PB-PHISH-001",
  "playbook_version": "1.0.0",
  "status": "opened",
  "severity": "medium",
  "created": "2026-11-09",
  "verdict": null,
  "confidence": null,
  "iocs": [],
  "findings": [],
  "conclusion": null,
  "limitations": [],
  "artifacts": []
}
```

## Notas

- Validar contra [`schemas/case.schema.json`](../../schemas/case.schema.json).
- Los artefactos se referencian por nombre logico, nunca por ruta local.
- Si el caso es real, no se publica: vive fuera del repositorio.
