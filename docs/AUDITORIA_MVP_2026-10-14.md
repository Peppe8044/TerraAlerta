# Auditoría de implementabilidad y confiabilidad — 14-10-2026

**Estado:** plan técnico auditado documentalmente; **ninguna integración de datos ni modelo está certificada, implementada o validada por este documento**. Alcance inicial: San José de Maipo.

## Definiciones (evitar la expresión «100 % confiable»)

- **Reproducible técnicamente:** mismos datos y software generan las mismas salidas en pruebas.
- **Fiel a la fuente:** el dato mostrado coincide con el recibido y conserva unidades, coordenadas, tiempo de emisión/observación y procedencia.
- **Confiabilidad científica:** requiere comparación independiente con observaciones y reporte de errores/incertidumbre.
- **Adecuación operativa:** requiere latencia, cobertura, mantenimiento y evaluación de seguridad aceptables.
- Ninguna de las anteriores garantiza predecir todos los eventos; nunca declarar una vivienda como «segura».

## Matriz de decisiones para Claude Code

| Componente | Estado de decisión | Condición de implementación | Prueba de aceptación |
|---|---|---|---|
| Mapa navegable y selección de coordenadas | **Implementar ya** | MapLibre y cartografía con términos de tiles compatibles | Punto elegido = punto consultado, accesibilidad y sin sobrecarga de tiles públicos |
| Resumen de ubicación y trazabilidad | **Implementar ya** | Modelo de datos uniforme; bandera de frescura y calidad | Toda cifra muestra fuente, hora, unidades, resolución y cobertura |
| Pronóstico 24/48/72 h | **Implementar en MVP** | Proveedor con licencia válida para fase no comercial; presupuesto de uso | Test contra respuesta API real, cálculo de acumulados y zona horaria |
| Lluvia observada NASA IMERG | **Implementar en MVP después de prueba de ingesta** | Earthdata cuando corresponda, dataset y latencia confirmados | No atribuir resolución kilométrica a parcela ni llamar tiempo real al Early |
| Estaciones DGA/DMC | **Piloto condicionado** | Verificar estaciones cercanas, períodos disponibles y condiciones de extracción | Comparación con observaciones emparejadas, huecos y sesgo documentados |
| DEM/pendiente | **MVP condicionado a licencia y resolución** | Verificar producto DEM 30/90 m y permisos vigentes | DEM reproyectado, unidades coherentes, incertidumbre por píxel |
| Quebradas e inventarios SERNAGEOMIN | **MVP condicionado a acceso/reutilización** | Verificación de WMS/WFS/descarga, capas, escala, vigencia y licencia | Presentar como referencia, no clasificación automática de viviendas |
| Eventos históricos | **Implementar base y esquema en MVP** | Incluir solo eventos corroborados y geolocalizados con calidad indicada | Cada evento incluye fecha, fuente, precisión y estado de verificación |
| Contenido SENAPRED | **Implementar en MVP** | Resumen atribuido y enlaces a orientación oficial vigente | Revisión editorial, versionado y no generar rutas de evacuación |
| NASA LHASA | **Investigación** | Cobertura/latencia/granularidad y permisos revisados | Comparación retrospectiva, nunca veredicto puntual |
| Google Flood Hub | **No es dependencia del MVP** | API requiere autorización; no extraer del visor sin permiso | Integración aislada con feature flag si autorizan |
| Notificaciones a usuarios | **Después del MVP** | Consentimiento, origen oficial diferenciado, evitar alarmas propias | Pruebas de lenguaje, latencia, cancelación y falsos positivos |
| ML de aluviones | **No operativo, solo investigación** | Etiquetas de eventos y no eventos; evaluación temporal y espacial | PR-AUC, sensibilidad, falsas alertas, calibración y baseline; revisión externa |
| Predicción predial o evacuación | **No implementar** | Evidencia/responsabilidad inexistentes a esta escala | Bloquear UI y API que afirmen estos resultados |

## Contrato de calidad obligatorio

Cada fuente documenta: propietario, URL, versión/producto, licencia exacta, redistribución permitida o no, modalidad comercial/no comercial, autenticación, costo, frecuencia, resolución espacial/temporal, latencia, cobertura, última comprobación y estado (`approved`, `research_only`, `blocked`). Una URL pública **no prueba** derecho de redistribución o uso comercial.

Cada medición expone: `value`, `unit`, `source_id`, `issued_at`, `observed_at` o `valid_time`, `retrieved_at`, `spatial_resolution`, `location_geometry`, `quality_flag`, `latency`, `limitations`.

Separar estrictamente observación / pronóstico / topografía / registro histórico / interpretación. `null` explícito si falta el dato; nunca rellenar con valores inventados. Pruebas para cortes de API, información obsoleta, reproyección, borde de celdas y cambio de hora Chile.

## Gates para publicar

- **G0 — Fuentes:** documentación de permisos/licencias y cobertura antes de activar conectores.
- **G1 — Ingesta:** ETL automático reproducible, trazabilidad, unidades, fechas y control de fallos.
- **G2 — Contraste:** IMERG y pronósticos comparados con estaciones disponibles; declarar error, sesgo, datos ausentes y representatividad espacial.
- **G3 — Territorio:** validar capas frente a cartografía oficial y escala de mapa; incertidumbre visible.
- **G4 — Comprensión y seguridad:** usuarios distinguen información experimental de alertas SENAPRED; ninguna recomendación da falsa seguridad.
- **G5 — Modelos predictivos futuros:** pruebas externas temporales/geográficas, revisión de expertos, tasa de falsas alarmas y calibración antes de despliegue.

## Entregables inmediatos para Claude Code

1. Crear `docs/FUENTES_ESTADO.md` como inventario vivo (fecha de última verificación, licencia, consulta de prueba, evidencia, responsable).
2. Implementar backend `/v1/sources` y un panel «¿De dónde viene este dato?» antes de mostrar cualquier evaluación.
3. Integrar 1 fuente real de pronóstico aprobada; marcar la interfaz como prototipo no comercial.
4. Incorporar un importador IMERG en modo investigación, con datos reproducibles de un intervalo histórico; no activar lluvia «en vivo» hasta verificar latencia.
5. Implementar un visor de eventos vacío con mensaje claro hasta que existan registros revisados; no simular aluviones reales.
6. Construir tests automáticos y un reporte de QA: funcionalidades funcionales, condicionadas, bloqueadas y pendientes.
7. No entrenar modelos ML de aluviones ni crear alarmas push en este sprint.

## Referencias principales para verificar términos antes de uso

- NASA IMERG: https://gpm.nasa.gov/data/imerg
- NASA GPM data policy: https://gpm.nasa.gov/data/policy
- Open-Meteo terms: https://open-meteo.com/en/terms
- Copernicus Data Space: https://dataspace.copernicus.eu/
- SERNAGEOMIN PortalGeomin: https://portalgeomin.sernageomin.cl/
- DGA: https://dga.mop.gob.cl/
- SENAPRED: https://www.senapred.cl/
- OpenStreetMap tile policy: https://operations.osmfoundation.org/policies/tiles/

**Regla de publicación:** el valor del MVP está en ofrecer fuentes trazables, información correcta sobre sus límites y orientación oficial; no proclamar precisión científica que aún no se midió.
