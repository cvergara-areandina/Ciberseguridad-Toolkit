# Ciberseguridad Toolkit

> Repositorio abierto de **playbooks**, **herramientas** y **esquemas** para análisis de seguridad.
> Contenido reutilizable por personas, agentes y modelos de lenguaje. Sin PII, sin dependencias externas.

[![CI](https://github.com/cvergara-areandina/Ciberseguridad-Toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/cvergara-areandina/Ciberseguridad-Toolkit/actions/workflows/ci.yml)
[![Estado](https://img.shields.io/badge/estado-dise%C3%B1o-yellow)]()
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-blue)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE-docs)

---

## Qué es

Una base de conocimiento operativa para atender casos de ciberseguridad:

- **Playbooks** — procesos de análisis paso a paso (phishing, malware, OSINT, respuesta a incidentes).
- **Herramientas** — scripts en Python (solo stdlib) que funcionan **offline**.
- **Esquemas** — contratos JSON para casos, reportes, IOCs y el manifiesto del repo.
- **Plantillas** — documentos listos para reutilizar.

## Para quién

| Público | Punto de entrada |
|---|---|
| 👤 Personas | [`README.md`](README.md) → [`INDEX.md`](INDEX.md) |
| 🤖 Modelos de lenguaje | [`llms.txt`](llms.txt) → [`manifest.json`](manifest.json) |
| ⚙️ Agentes / automatización | [`AI.md`](AI.md) → [`schemas/`](schemas/) |

## Inicio rápido

```bash
git clone https://github.com/cvergara-areandina/Ciberseguridad-Toolkit.git
cd Ciberseguridad-Toolkit

# Ver el indice completo
cat INDEX.md

# Ejecutar una herramienta (sin instalar nada)
python tools/<dominio>/<herramienta>.py --help
```

No se requiere `pip install`. Todas las herramientas usan la biblioteca estándar de Python 3.9+.

## Estructura

```
.
├── README.md          Entrada principal
├── INDEX.md           Menu maestro (humanos)
├── llms.txt           Indice curado (LLMs)
├── manifest.json      Indice estructurado (maquinas)
├── AGENTS.md          Instrucciones para agentes
├── docs/              Metodologia, convenciones, plantillas
├── playbooks/         Procesos de analisis
├── tools/             Herramientas ejecutables
├── schemas/           Contratos JSON
├── examples/          Casos ficticios de ejemplo
└── casos/             Indice de casos (sin datos reales)
```

## Principios

1. **Offline primero.** Ninguna herramienta accede a la red salvo con `--online` explícito.
2. **Sin PII.** El repositorio contiene método, nunca datos de casos reales.
3. **Determinista.** Mismas entradas, mismas salidas. Salida `--json` en toda herramienta.
4. **Legible por máquinas.** Front-matter validado, IDs estables, esquemas versionados.

## Cómo contribuir

Lee [`CONTRIBUTING.md`](CONTRIBUTING.md) y [`docs/convenciones/`](docs/convenciones/).

## Seguridad

Para reportar vulnerabilidades, consulta [`SECURITY.md`](SECURITY.md). **No abras issues públicos con datos sensibles.**

## Licencia

- **Codigo** (`tools/`): [MIT](LICENSE) — uso, copia, modificacion y redistribucion libres.
- **Documentacion** (`playbooks/`, `docs/`): [CC BY 4.0](LICENSE-docs) — reutilizable citando la fuente.

> ⚠️ Estado: **esqueleto en construcción**. Ver [`CHANGELOG.md`](CHANGELOG.md).
