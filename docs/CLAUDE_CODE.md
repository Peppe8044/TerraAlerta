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
