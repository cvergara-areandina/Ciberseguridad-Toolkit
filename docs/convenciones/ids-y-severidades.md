---
id: DOC-CONV-001
type: doc
title: Convencion de IDs y severidades
summary: Identificadores estables e inmutables y escala unica de criticidad para todo el repositorio.
tags: [conventions, severity, ids]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Convencion de IDs y severidades

## Identificadores

Formato: `<PREFIJO>-<DOMINIO>-<NNN>`

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `PB` | Playbook | `PB-PHISH-001` |
| `DOC` | Documento | `DOC-CONV-001` |
| `TOOL` | Herramienta | `TOOL-FOR-001` |
| `SCH` | Esquema | `SCH-001` |
| `TPL` | Plantilla | `TPL-001` |
| `EX` | Ejemplo | `EX-001` |
| `CASE` | Caso | `CASE-2026-001` |

### Reglas

1. **Inmutable.** Un ID nunca se reutiliza ni se renombra.
2. **Secuencial por dominio.** No se rellenan huecos.
3. **Un ID, un recurso.** Si un recurso se divide, los nuevos reciben IDs nuevos.
4. **El ID va en el front-matter y en el indice**, nunca solo en el nombre del archivo.

## Escala de severidad

| Nivel | Criterio | Plazo sugerido |
|---|---|---|
| `critical` | Compromiso activo, datos expuestos o impacto operativo total | Inmediato |
| `high` | Explotable con condiciones reales, impacto alto | 24-72 h |
| `medium` | Requiere condiciones especificas o impacto limitado | 1-2 semanas |
| `low` | Riesgo menor o higiene de seguridad | 30 dias |
| `info` | Observacion sin riesgo directo | Sin plazo |

## Estados de un caso

| Estado | Significado |
|---|---|
| `opened` | Creado, sin analisis |
| `in_progress` | En analisis |
| `pending_user` | Esperando informacion o decision |
| `resolved` | Concluido |
| `escalated` | Requiere intervencion externa |
| `false_alarm` | No era una amenaza |

## Clasificacion de red

| Valor | Significado | Autorizacion |
|---|---|---|
| `none` | 100% offline | No requiere |
| `optional` | Consulta externa opcional | Requiere confirmacion |
| `required` | Internet obligatorio | Requiere confirmacion |
