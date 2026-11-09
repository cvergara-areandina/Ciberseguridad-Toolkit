---
id: PB-PII-001
type: playbook
title: Auditoria de PII
summary: Detecta datos personales, credenciales y configuracion hardcodeada en archivos locales.
tags: [pii, privacy, audit, compliance, secrets]
network: none
inputs: [archivo_xml, archivo_json, archivo_yaml, codigo_fuente]
outputs: [inventario_de_datos_sensibles, hallazgos, recomendaciones]
tools: [tools/ioc/ioc_extractor.py]
severity_scope: [critical, high, medium, low]
version: 1.0.0
status: draft
last_reviewed: 2026-11-09
license: CC-BY-4.0
---

# Auditoria de PII

## Cuando usarlo

Antes de publicar un repositorio, compartir un archivo o auditar cumplimiento.

## Categorias a buscar

| Categoria | Patron | Ejemplo |
|---|---|---|
| Email | `usuario@dominio.tld` | `persona@ejemplo.com` |
| Telefono | Digitos con separadores | `+00 000 000 0000` |
| Documento | CLABE, cuenta, tarjeta, RFC, CURP, RUT, NIT | Secuencias numericas validadas |
| Nombre | Nombres completos en datos de prueba | `Nombre Apellido Apellido` |
| Credencial | API keys, tokens, passwords | `sk-...`, `Bearer ...` |
| Direccion | Calle, codigo postal, ciudad | `Calle 000, Col. Centro` |
| URL interna | IPs privadas, hosts internos | `http://10.0.0.1/api` |
| Estructura | Nombres de campo sensibles | `cardnumber`, `cvv`, `clientkey` |

## Pasos

### 1. Inventario

Lista los archivos a auditar y su origen.

### 2. Extraccion local

```bash
python tools/ioc/ioc_extractor.py --file objetivo.xml --json --pii
```

Todo el procesamiento es local. No enviar contenido a servicios externos.

### 3. Clasificacion

| Criticidad | Criterio |
|---|---|
| `critical` | Credenciales activas o datos financieros |
| `high` | Identificadores personales directos |
| `medium` | Nombres, telefonos, direcciones |
| `low` | Estructura de datos sin valores reales |

### 4. Falsos positivos

Descarta hashes, base64, SVG y binarios antes de reportar.

### 5. Reporte

Ubicacion exacta por hallazgo: archivo, linea o ruta logica dentro del documento.

## Regla de salida

El reporte **nunca** reproduce el dato completo. Se muestra enmascarado:

```
persona@ejemplo.com  ->  p*****@e*****.com
```

## Limitaciones

- Los patrones genericos producen falsos positivos.
- Sin diccionario de nombres no se detectan todos los nombres propios.
- No sustituye una revision manual en datos regulados.
