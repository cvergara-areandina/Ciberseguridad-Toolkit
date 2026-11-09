---
id: PB-PHISH-001
type: playbook
title: Triage de phishing
summary: Clasifica un correo sospechoso, verifica autenticacion y extrae indicadores accionables.
tags: [phishing, email, triage, ioc, spf, dkim, dmarc]
network: none
inputs: [archivo_eml, cabeceras_copiadas, texto_del_correo]
outputs: [veredicto, confianza, iocs, hallazgos, limitaciones]
tools: [tools/forense/email_header_parser.py, tools/recon/url_analyzer.py, tools/ioc/ioc_extractor.py]
severity_scope: [critical, high, medium, low, info]
version: 1.0.0
status: stable
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Triage de phishing

## Cuando usarlo

- Un usuario reporta un correo sospechoso.
- Hay que decidir si un mensaje es legitimo, sospechoso o malicioso.
- Se necesita extraer IOCs para bloquear o correlacionar.

## Requisitos

- El archivo `.eml` completo. **Sin `.eml` no se puede verificar autenticacion.**
- Ejecutar siempre en local. No abrir enlaces ni adjuntos.

## Pasos

### 1. Preservar evidencia

Calcula el hash antes de tocar nada:

```bash
python tools/forense/hash_tools.py --file correo.eml
```

Anota SHA-256. Es la referencia de integridad del caso.

### 2. Analizar cabeceras

```bash
python tools/forense/email_header_parser.py correo.eml --json
```

Verifica en este orden:

| Control | Que mirar | Bandera roja |
|---|---|---|
| `Received` | Cadena de servidores, de abajo arriba | Saltos inesperados o IPs residenciales |
| `Return-Path` | Debe alinear con `From` | Dominio distinto |
| `Authentication-Results` | SPF, DKIM, DMARC | `fail` o ausente |
| `From` / `Reply-To` | Coincidencia | `Reply-To` a dominio externo |
| `Message-ID` | Formato del proveedor | Formato generico o malformado |
| `X-Mailer` | Cliente usado | Scripts de envio masivo |

### 3. Analizar URLs

```bash
python tools/recon/url_analyzer.py --file urls.txt --json
```

Busca: typosquatting, punycode, acortadores, IPs literales, parametros con tokens,
subdominios anidados (`banco.com.evil.tld`).

### 4. Analizar adjuntos

- Calcula hash y consulta reputacion **solo con autorizacion** (requiere red).
- No ejecutes nunca el adjunto.
- Tipos de riesgo: `.exe`, `.scr`, `.js`, `.lnk`, `.iso`, `.html` con scripts, macro en Office.

### 5. Extraer IOCs

```bash
python tools/ioc/ioc_extractor.py --file correo.eml --json --defang
```

### 6. Emitir veredicto

| Veredicto | Criterio |
|---|---|
| `legitimo` | Autenticacion pasa, URLs del dominio real, sin adjuntos raros |
| `sospechoso` | Senales contradictorias o autenticacion no verificable |
| `phishing` | Suplantacion demostrable, credenciales solicitadas, dominio falso |
| `indeterminado` | Evidencia insuficiente (p. ej. sin cabeceras) |

## Salida esperada

```json
{
  "playbook": "PB-PHISH-001",
  "playbook_version": "1.0.0",
  "verdict": "sospechoso",
  "confidence": "medium",
  "iocs": [],
  "findings": [],
  "limitations": []
}
```

## Errores comunes

- **Confundir "no verificable" con "malicioso".** Si faltan cabeceras, el veredicto es `indeterminado`, no `phishing`.
- **Confiar en el nombre mostrado del remitente.** Solo cuenta el dominio real.
- **Abrir enlaces para "ver que pasa".** Analiza estaticamente.

## Limitaciones

- No sustituye un sandbox para adjuntos.
- Sin `Authentication-Results` no hay verificacion criptografica.
- Reputacion de dominios requiere red y autorizacion.
