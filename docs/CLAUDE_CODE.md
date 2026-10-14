# Instrucción de implementación para Claude Code

Actúa como arquitecto e ingeniero senior full stack y geoespacial. Implementa el MVP de TerraAlerta Chile siguiendo `README.md` y `docs/{PRODUCTO,DATOS,ARQUITECTURA,VALIDACION}.md`. El objetivo es un prototipo real y auditable para San José de Maipo, no una demostración visual con datos inventados.

Orden obligatorio:
1. Inspecciona la estructura, escribe un plan corto y una matriz de fuentes (acceso, licencias, fechas, límites). Si una fuente no es legalmente reutilizable o no funciona, registra `blocked`, ofrece alternativa y no inventes respuestas.
2. Genera monorepo Next.js/TypeScript + MapLibre + FastAPI/Python + PostGIS y Docker Compose, `.env.example`, `.gitignore`, tests y CI.
3. Crea fixtures únicamente para pruebas etiquetadas `synthetic`; evita mostrar números sintéticos como datos reales en la UI.
4. Integra primero un proveedor real y verificable de pronóstico no comercial, con parser, metadatos, retries, caché y manejo de fallos. Después añade DEM y lluvia reciente con control de escala y licencia.
5. Desarrolla mapa navegable con selección por punto, gráficos sencillos y panel de trazabilidad, limitaciones y enlace a SENAPRED.
6. Implementa validaciones de fuentes y pruebas unitarias/integración para fechas, unidades, geometrías y fallos.
7. Deja `docs/DECISIONES.md` con decisiones, bloqueos y siguientes pasos de investigación; evita entrenar ML hasta conocer etiquetas y baselines válidos.

Criterios de aceptación: `docker compose up` inicia componentes, `/health` responde, selección en mapa funciona, la app no llama «riesgo» a una estadística no validada, todas las cifras reales exhiben fuente y fecha, y tests pasan. No introduzcas APIs pagadas ni publiques datos sensibles.

## Requisito adicional — prevención ante aluviones

Antes de implementar, leer `docs/ALUVIONES_Y_PREVENCION.md` e incorporar su matriz P0/P1/P2 al plan. En P0 añadir historial de eventos documentados, contexto de quebradas/pendientes, información sobre lluvia reciente con fechas y una ficha de preparación respaldada por SENAPRED. No construir notificaciones ni reportes ciudadanos hasta pasar sus puertas de validación. Aceptar «datos insuficientes» y no mostrar riesgo numérico, sectores «seguros» ni rutas de evacuación inferidas.

## Gate de confiabilidad obligatorio (14-10-2026)

Leer `docs/AUDITORIA_MVP_2026-10-14.md` antes de codificar. Crear `docs/FUENTES_ESTADO.md` y ejecutar los gates G0–G4 para la versión informativa. Priorizar mapa, trazabilidad, pronóstico de fuente autorizada y orientación SENAPRED. Integraciones IMERG, DEM, DGA y SERNAGEOMIN solo tras revisar sus permisos, cobertura y precisión; mantener conectores deshabilitados si falta aprobación. No introducir ML de aluviones, «sectores seguros», alertas de evacuación ni porcentajes de riesgo predial en el MVP.

## Roadmap ampliado de valor ciudadano

Leer `docs/ROADMAP_VALOR_CIUDADANO.md` antes de planificar sprints. Consolidar con `docs/ALUVIONES_Y_PREVENCION.md`, evitando duplicar checklist y capas. Implementar primero checklist de preparación local y pantallas de observaciones DGA e históricos **solo si las fuentes cumplen G0/G1**; usar estados sin datos cuando corresponda. Registrar decisiones y resultados de pruebas. Mantener Sentinel-1, asistente IA y datos privados de predios como fases posteriores sujetas a validación.
