# Contribuir

Gracias por aportar al Ciberseguridad Toolkit.

## Antes de empezar

1. Lee [`docs/convenciones/front-matter.md`](docs/convenciones/front-matter.md).
2. Revisa [`docs/convenciones/ids-y-severidades.md`](docs/convenciones/ids-y-severidades.md).
3. Verifica que tu aporte **no contiene datos personales ni secretos**.

## Ramas

| Rama | Uso |
|---|---|
| `main` | Estable. Protegida. |
| `feature/<nombre>` | Nueva herramienta, playbook o documento |
| `hotfix/<nombre>` | Correccion urgente |
| `release/<x.y.z>` | Preparacion de version (solo si se empaqueta) |

## Commits

Conventional Commits:

```
feat(playbook): anadir playbook de ransomware
fix(tools): corregir calculo de entropia
docs(convenciones): aclarar formato de IDs
chore(ci): actualizar validador
```

## Pull request

- Un cambio por PR.
- Descripcion: que, por que y como se probo.
- Si anades un recurso: actualiza `INDEX.md`, `llms.txt` y `manifest.json`.
- El CI debe pasar (front-matter, esquemas, tests, gitleaks).

## Checklist

- [ ] Sin PII ni secretos
- [ ] Front-matter completo
- [ ] ID unico
- [ ] `python tools/gestion/validate_repo.py` pasa
- [ ] `python -m pytest tools/tests -q` pasa
- [ ] Documentacion actualizada

## Estilo

- Markdown con un solo `#` por documento.
- Espanol neutro, sin regionalismos.
- Codigo Python con type hints y sin dependencias externas.
