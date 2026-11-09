# AGENTS.md — Ciberseguridad Toolkit

Instrucciones para agentes y modelos de lenguaje que operen sobre este repositorio.

## Proposito

Repositorio abierto de **playbooks**, **herramientas** y **esquemas** para analisis de seguridad.
Contenido reutilizable por personas, agentes y LLM. Sin datos personales, sin dependencias externas.

## Regla de oro: privacidad

1. **Antes de cualquier accion**, indica si es `LOCAL`, `HIBRIDO` o `EXTERNO`.
2. Indica **que datos se exponen**.
3. Ofrece una **alternativa local** si existe.
4. **Espera autorizacion explicita** antes de cualquier salida a internet.

Ninguna herramienta de este repositorio accede a la red sin `--online`.

## Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `README.md` | Entrada para personas |
| `INDEX.md` | Menu maestro |
| `llms.txt` | Indice curado para LLM |
| `manifest.json` | Indice estructurado (maquina) |
| `AI.md` | Como consumir el repo desde una IA |
| `docs/` | Metodologia, convenciones y plantillas |
| `playbooks/` | Procedimientos paso a paso |
| `tools/` | Herramientas ejecutables (stdlib) |
| `schemas/` | Contratos JSON |
| `examples/` | Casos ficticios |
| `casos/` | Indice de casos sin PII |

## Orden de lectura

1. `llms.txt`
2. `manifest.json`
3. `playbooks/<id>.md`
4. `schemas/`

## Reglas de operacion

- **No inventes rutas**: usa solo las listadas en `manifest.json`.
- **Respeta el contrato**: toda salida estructurada valida contra `schemas/`.
- **Offline por defecto**: si el recurso declara `network: optional|required`, pide autorizacion.
- **Sin PII**: nunca escribas datos personales reales, correos, telefonos ni credenciales.
- **Defang**: comparte indicadores como `ejemplo[.]com`, `hxxps://`.
- **No ejecutes muestras**: analiza estaticamente o en entorno aislado.

## Contrato de herramientas

Toda herramienta en `tools/` debe:

1. Aceptar `--help` y `--json`.
2. Funcionar offline salvo `--online` explicito.
3. Usar solo la biblioteca estandar de Python 3.10+.
4. Devolver codigos de salida `0` (exito), `1` (sin hallazgos), `2` (error de uso).
5. Declarar su bloque de metadatos (`id`, `type`, `network`, `version`, `status`) al inicio del archivo.

## Anadir contenido

1. Copia la plantilla correspondiente (`playbooks/_template.md` o `docs/plantillas/`).
2. Asigna un ID nuevo segun `docs/convenciones/ids-y-severidades.md`.
3. Completa el front-matter segun `docs/convenciones/front-matter.md`.
4. Ejecuta:

```bash
python tools/gestion/build_manifest.py
python tools/gestion/validate_repo.py
python -m pytest tools/tests -q
```

## Formato de respuesta

Cuando uses un playbook, produce JSON validable:

```json
{
  "playbook": "PB-XXXX-001",
  "playbook_version": "1.0.0",
  "verdict": "",
  "confidence": "low",
  "iocs": [],
  "evidence": [],
  "limitations": []
}
```

## Convenciones de codigo

- Python 3.10+, type hints, sin dependencias externas.
- Encoding UTF-8 sin BOM.
- Fin de linea LF (ver `.gitattributes`).
- PowerShell con CRLF.

## Prohibiciones

- Ejecutar comandos destructivos sin confirmacion.
- Publicar secretos, credenciales o PII.
- Enviar datos de casos a servicios externos sin autorizacion.
- Modificar `manifest.json` a mano: se genera con `build_manifest.py`.
