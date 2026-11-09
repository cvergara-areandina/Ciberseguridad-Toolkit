# Consumo del repositorio por agentes e IA

Guia para que un agente, LLM o pipeline automatizado use este repositorio sin ambiguedad.

## Orden de lectura recomendado

1. **`llms.txt`** — indice curado y corto. Empieza aqui.
2. **`manifest.json`** — indice estructurado con metadatos por recurso.
3. **`AGENTS.md`** — reglas de operacion y limites.
4. **`playbooks/<id>.md`** — procedimiento concreto (front-matter + pasos).
5. **`schemas/`** — contrato de los datos que vas a producir o validar.

## Reglas de operacion para agentes

| Regla | Detalle |
|---|---|
| Ejecuta offline | Toda herramienta es `network: none` por defecto. |
| Pide permiso antes de red | Si el playbook declara `network: optional` o `required`, solicita autorizacion explicita. |
| No inventes rutas | Usa solo rutas listadas en `manifest.json`. |
| Respeta el contrato | Toda salida estructurada debe validar contra `schemas/`. |
| No publiques PII | Ningun archivo de este repo debe contener datos personales reales. |

## Formato de respuesta esperado

Cuando uses un playbook, produce:

```json
{
  "playbook": "PB-PHISH-001",
  "playbook_version": "1.0.0",
  "verdict": "phishing | legitimo | sospechoso | indeterminado",
  "confidence": "low | medium | high",
  "iocs": [],
  "evidence": [],
  "limitations": []
}
```

Valida el resultado contra [`schemas/case.schema.json`](schemas/case.schema.json).

## Uso como fuente de conocimiento (RAG)

- Fragmenta por seccion `##` de cada playbook.
- Usa `id` + `version` del front-matter como clave de cache.
- Descarta el bloque de front-matter del texto indexado (es metadato).
- El campo `network` determina si el contenido requiere conectividad.

## Uso como herramienta

```bash
python tools/<dominio>/<script>.py --help      # ayuda
python tools/<dominio>/<script>.py --json ...  # salida parseable
```

Codigos de salida: `0` exito · `1` hallazgo negativo · `2` error de uso.

## Limitaciones conocidas

- Los scripts no incluyen analisis dinamico real de malware.
- Las consultas a inteligencia externa requieren claves propias.
- El repositorio no almacena evidencia: solo metodo.
