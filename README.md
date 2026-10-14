# TerraAlerta Chile

**Estado:** especificación inicial / MVP experimental. **Fecha:** 14 de octubre de 2026.

TerraAlerta Chile es una plataforma experimental de inteligencia territorial que combina lluvia observada, pronóstico y características geográficas para explicar **condiciones que pueden aumentar la vulnerabilidad frente a lluvias extremas y deslizamientos**. No predice inundaciones a nivel de vivienda, no emite alertas oficiales y no sustituye a SENAPRED.

## Alcance MVP

Piloto: **San José de Maipo, Región Metropolitana**. Aplicación web adaptada a móviles. Seleccionar punto en mapa y ver: pronóstico de lluvia a 24/48/72 h, lluvia reciente (cuando haya fuente válida), pendiente y proximidad a drenajes/cursos de agua, procedencia/actualización de cada dato, y ficha de condiciones observadas con incertidumbres. La evaluación inicial será **descriptiva**, no una probabilidad calibrada de desastre. Un módulo experimental de deslizamientos podrá incorporarse solo después de validar cobertura y resultados.

## Primeros pasos con Claude Code

1. Leer `docs/PRODUCTO.md`, `docs/DATOS.md`, `docs/ARQUITECTURA.md`, `docs/VALIDACION.md` y `docs/CLAUDE_CODE.md`.
2. Crear monorepo con `/apps/web`, `/services/api`, `/pipelines`, `/infra`, `/tests`, `/docs`.
3. Implementar primero un *demo reproducible* con datos de prueba claramente marcados y luego conectores reales, sin inventar observaciones.
4. En ningún entorno mostrar una puntuación de riesgo numérica no validada.
5. Usar secretos mediante variables de entorno; nunca incluir credenciales o coordenadas de predios privados en el repositorio.

## Licencia

No se ha elegido aún licencia para el código original. No asumir que las licencias de terceros se extienden automáticamente al código o a productos derivados. Consultar `docs/DATOS.md`.
