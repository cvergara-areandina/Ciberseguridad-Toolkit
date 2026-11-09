---
id: PB-IR-001
type: playbook
title: Respuesta a incidentes
summary: Contencion, erradicacion y recuperacion ante un incidente confirmado o probable.
tags: [incident-response, containment, forensics, recovery]
network: none
inputs: [descripcion_del_incidente, evidencia_inicial]
outputs: [plan_de_contencion, acciones_de_erradicacion, lecciones_aprendidas]
tools: [tools/gestion/session_manager.py]
severity_scope: [critical, high, medium]
version: 1.0.0
status: draft
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Respuesta a incidentes

## Cuando usarlo

Hay indicios de compromiso: cuenta comprometida, malware activo, exfiltracion o acceso no autorizado.

## Fases

### 1. Preparacion

- Identifica roles, canales y criterios de escalado.
- Define que se preserva antes de tocar sistemas.

### 2. Identificacion

- Alcance: que sistemas, cuentas y datos estan afectados.
- Preserva evidencia volatil primero (memoria, conexiones, procesos).

### 3. Contencion

| Tipo | Accion | Riesgo |
|---|---|---|
| Corto plazo | Aislar host, revocar sesiones | Perdida de evidencia si se apaga |
| Largo plazo | Segmentar red, rotar credenciales | Interrupcion de servicio |

> Nunca apagues un equipo sin decidir antes si necesitas memoria volatil.

### 4. Erradicacion

- Elimina persistencia, cuentas creadas y artefactos maliciosos.
- Verifica que la causa raiz esta cerrada.

### 5. Recuperacion

- Restaura desde copias verificadas.
- Monitoriza durante un periodo definido.

### 6. Lecciones aprendidas

- Que fallo, que funciono, que se cambia.

## Registro

Cada accion con hora, responsable y resultado. Sin esto no hay forense defendible.

## Limitaciones

- Este playbook no sustituye a un equipo legal o de cumplimiento.
- La preservacion de evidencia requiere cadena de custodia formal.
