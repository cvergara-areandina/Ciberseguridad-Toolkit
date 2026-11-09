---
id: TPL-001
type: template
title: Plantilla de reporte de analisis
summary: Estructura base para documentar un analisis de seguridad sin datos personales.
tags: [template, report]
network: none
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Reporte de analisis — {ID}

## 1. Resumen ejecutivo

Tres lineas como maximo: que se analizo, que se encontro y que se recomienda.

## 2. Datos del caso

| Campo | Valor |
|---|---|
| ID | CASE-AAAA-NNN |
| Playbook | PB-XXXX-001 v1.0.0 |
| Fecha | AAAA-MM-DD |
| Analista | (seudonimo o rol) |
| Clasificacion | publico / interno / confidencial |

## 3. Evidencia analizada

| Artefacto | Tipo | Hash (SHA-256) | Origen |
|---|---|---|---|
| | | | |

> No incluir rutas locales absolutas ni nombres de personas.

## 4. Hallazgos

| # | Hallazgo | Severidad | Ubicacion |
|---|---|---|---|
| 1 | | | |

## 5. Indicadores (IOCs)

| Tipo | Valor (defanged) | Contexto |
|---|---|---|
| domain | `ejemplo[.]com` | |

## 6. Limitaciones

- Que no se pudo verificar y por que.

## 7. Recomendaciones

| Prioridad | Accion | Responsable |
|---|---|---|
| Alta | | |

## 8. Conclusion

Veredicto, nivel de confianza y siguiente paso.
