# Politica de seguridad

## Reportar una vulnerabilidad

**No abras un issue publico** con datos sensibles.

Envia un correo al mantenedor indicando:

- Descripcion del problema y componente afectado.
- Pasos de reproduccion.
- Impacto estimado.
- Si lo deseas, tu nombre para el reconocimiento.

Plazo de respuesta objetivo: 72 horas.

## Alcance

Aplica a:

- Codigo de `tools/`.
- Esquemas de `schemas/`.
- Contenido de `playbooks/` y `docs/`.

## Fuera de alcance

- Vulnerabilidades en servicios de terceros (VirusTotal, AbuseIPDB).
- Ataques a infraestructura del proyecto.

## Reglas del repositorio

1. **Nunca** subir evidencia real, muestras de malware ni credenciales.
2. **Nunca** ejecutar muestras fuera de un entorno aislado.
3. Los enlaces se documentan siempre en formato defanged.
4. Los scripts no acceden a la red salvo con `--online` explicito.

## Datos personales

Si encuentras PII en el repositorio, reportalo de inmediato. Se eliminara del historial
y se rotaran las credenciales si corresponde.
