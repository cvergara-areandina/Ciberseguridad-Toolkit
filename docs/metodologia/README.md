# Metodologia

Como se trabaja en este repositorio.

## Ciclo de vida de un playbook

1. **Borrador** (`status: draft`) — se escribe el procedimiento.
2. **Revision** (`status: review`) — se prueba con un caso ficticio en `examples/`.
3. **Estable** (`status: stable`) — validado y referenciado en `manifest.json`.
4. **Deprecado** (`status: deprecated`) — se conserva por trazabilidad.

## Ciclo de vida de un caso

```
opened -> in_progress -> resolved
                     -> escalated
                     -> pending_user -> in_progress
                     -> false_alarm
```

## Regla de separacion

| Contenido | Donde vive |
|---|---|
| Metodo, plantillas, herramientas | **En el repositorio** (publico) |
| Evidencia, muestras, datos reales | **Fuera del repositorio** (local) |

## Revision periodica

- Cada playbook declara `last_reviewed`.
- Si supera 12 meses, pasa a `review`.
- El CI avisa de documentos caducados.

## Trazabilidad

- Cada cambio relevante va en `CHANGELOG.md`.
- Cada release lleva tag `vX.Y.Z`.
- Cada playbook lleva su propia `version`, independiente del repo.
