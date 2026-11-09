---
id: PB-OSINT-001
type: playbook
title: OSINT
summary: Reconocimiento pasivo de dominios, IPs y personas usando solo fuentes abiertas.
tags: [osint, recon, dns, whois, passive]
network: optional
inputs: [dominio, ip, nombre_de_usuario]
outputs: [superficie_de_exposicion, infraestructura, iocs, limitaciones]
tools: [tools/recon/network_utils.py, tools/recon/url_analyzer.py]
severity_scope: [high, medium, low, info]
version: 1.0.0
status: draft
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# OSINT

## Cuando usarlo

Se necesita conocer la huella publica de un objetivo antes de un analisis o evaluacion.

## Advertencia de privacidad

Este playbook tiene `network: optional`. **Toda consulta externa revela el objetivo a terceros**
(DNS, WHOIS, motores de busqueda). Solicita autorizacion explicita antes de ejecutar.

## Pasos

### 1. Reconocimiento pasivo (sin contacto)

- Registros DNS historicos y actuales.
- WHOIS y fechas de registro.
- Certificados TLS (transparencia de certificados).
- Tecnologias detectables por cabeceras publicas.

### 2. Enumeracion de superficie

| Activo | Fuente | Riesgo |
|---|---|---|
| Subdominios | DNS, CT logs | Servicios olvidados |
| Correos | Paginas publicas | Phishing dirigido |
| Empleados | Redes profesionales | Ingenieria social |

### 3. Analisis de exposicion

Clasifica cada hallazgo por sensibilidad y recomienda mitigacion.

### 4. Documentacion

Solo hechos verificables. Marca explicitamente lo inferido.

## Etica y limites

- Solo fuentes publicas. Nada de acceso no autorizado.
- No interactuar con el objetivo.
- No almacenar datos personales de terceros en el repositorio.

## Limitaciones

- Resultados dependen de la fuente y cambian con el tiempo.
- Sin red, este playbook solo produce el plan de recoleccion.
