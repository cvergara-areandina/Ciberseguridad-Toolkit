---
id: DOC-CONV-002
type: doc
title: Front-matter obligatorio
summary: Metadatos que todo documento del repositorio debe declarar al inicio del archivo.
tags: [conventions, metadata, yaml]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Front-matter obligatorio

Todo documento en `playbooks/`, `docs/` y `examples/` empieza con un bloque YAML delimitado por `---`.
El validador `tools/gestion/validate_repo.py` lo comprueba en cada commit.

## Plantilla

```yaml
---
id: PB-XXXX-001
type: playbook
title: Titulo corto
summary: Una sola frase de 20 a 200 caracteres que explique que resuelve.
tags: [tag1, tag2]
network: none
inputs: [tipo_de_entrada]
outputs: [tipo_de_salida]
tools: [tools/dominio/herramienta.py]
version: 1.0.0
status: draft
last_reviewed: 2026-11-09
license: CC-BY-4.0
---
```

## Campos

| Campo | Obligatorio | Descripcion |
|---|---|---|
| `id` | Si | Identificador estable (ver `ids-y-severidades.md`). |
| `type` | Si | `playbook`, `doc`, `template`, `example`. |
| `title` | Si | Maximo 80 caracteres. |
| `summary` | Si | Una frase. Se indexa en `llms.txt` y en RAG. |
| `tags` | Si | Minusculas y guiones. |
| `network` | Si | `none`, `optional`, `required`. |
| `inputs` | Playbooks | Que recibe. |
| `outputs` | Playbooks | Que produce. |
| `tools` | No | Herramientas que usa. |
| `version` | Si | Semver del documento, independiente del repo. |
| `status` | Si | `draft`, `review`, `stable`, `deprecated`. |
| `last_reviewed` | Si | Fecha ISO `YYYY-MM-DD`. |
| `license` | Si | Licencia del contenido. |

## Reglas

1. **No usar `:` sin comillas** en valores que lo contengan.
2. **No incluir PII** en ningun campo, tampoco en ejemplos.
3. **`summary` es contrato**: se muestra en indices; no lo cambies sin actualizar `manifest.json`.
4. **`version` sube** con cambios de fondo; las correcciones tipograficas no lo requieren.
