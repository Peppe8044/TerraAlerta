# Extensión: aluviones, remociones en masa e impacto territorial

Fecha: 14-10-2026. Estado: **especificación propuesta, no implementada**.

## Propósito
Ayudar a personas de San José de Maipo y la precordillera de Santiago a comprender condiciones meteorológicas y amenazas territoriales conocidas, preparar acciones preventivas y consultar fuentes oficiales. No pronosticar el colapso de una ladera ni reemplazar alertas de SENAPRED.

## Capacidades y prioridad

### P0 — MVP viable

**A. Lluvia observada y prevista por zona.** Vista de acumulaciones observadas (1/6/24/72 h si la fuente lo soporta), pronósticos 24/48/72 h y anomalías históricas solo cuando existan series comparables. Cada dato indica fuente, cobertura, resolución, hora de observación, fecha de emisión, latencia y limitaciones. No denominar «tiempo real» a series diferidas. No activar umbrales operacionales no avalados por especialistas.

**B. Mapa de susceptibilidad y antecedentes.** Capas de elevación, pendiente, cursos de agua/quebradas y, cuando exista autorización y calidad suficiente, inventarios oficiales de remociones en masa y cartografía de amenazas. Diferenciar **susceptibilidad estática** de amenaza dinámica por lluvias. Un lugar sin registros NO se declara seguro. No usar la cercanía a una quebrada como sustituto de evaluación hidrológica.

**C. Ficha de ubicación y preparación.** Al seleccionar punto, mostrar «factores a considerar», explicaciones y enlaces a SENAPRED, DMC y autoridad local; lista básica de preparación basada en fuentes oficiales, sin rutas de evacuación generadas automáticamente. No pedir registro para consulta pública. Diseño accesible, español claro, lectura móvil.

**D. Historial de eventos.** Visor de eventos documentados con fecha, ubicación aproximada, fuente, tipo (aluvión, remoción, inundación), certeza de geolocalización y antecedentes disponibles. No usar noticias como observaciones instrumentales sin corroboración. El registro de Las Condes de octubre de 2026 queda como **candidato por verificar** y no debe incorporarse como etiqueta de entrenamiento sin fuente oficial/localización verificada.

### P1 — Después de validar el MVP

**E. Predios y exposición.** Guardar opcionalmente ubicaciones de terrenos, mostrar qué capas intersectan su área y recomendaciones generales; consentimiento explícito y protección de coordenadas. No calcular seguridad a escala de vivienda con datos kilométricos.

**F. Notificaciones informativas.** Avisar de nueva información meteorológica relevante o de actualizaciones oficiales citadas literalmente/con atribución. Separar visual y semánticamente «información experimental» de «alerta oficial». Control de preferencias, consentimiento, desuscripción, latencia y rate limit. Sin órdenes de evacuación propias.

### P2 — Investigación y gobernanza

**G. Reportes ciudadanos.** Foto, localización opcional, fecha, categoría, verificación, moderación, privacidad y mecanismo de abuso. No publicar evidencia privada ni mostrar reportes no verificados como hechos. Usuario debe reportar desde lugar seguro, sin acercarse a quebradas peligrosas.

**H. Evaluación dinámica con machine learning.** Investigar características lluvia-intensidad-duración, acumulada antecedente, geometría de cuencas, suelo/geología y otros predictores medibles. Requiere etiquetas positivas y negativas, separación temporal/geográfica, controles de leakage, calibración y evaluación independiente. Jamás desplegar porcentajes de probabilidad sin validación sólida.

## Recorridos de usuario

1. **Consulta vecinal:** abrir web móvil → buscar dirección/comuna → seleccionar sector → ver precipitación observada/prevista y mapa con fuentes → leer «qué significa» y recomendaciones SENAPRED → compartir URL pública sin datos de usuario.
2. **Consulta histórica:** seleccionar zona → activar «Eventos históricos» → tocar un evento → ver fecha, atribución y calidad de geolocalización → consultar fuentes.
3. **Consulta de predio futura:** iniciar sesión voluntaria → delimitar parcela → aceptar uso de ubicación → recibir ficha territorial y preparar checklist; sin afirmaciones de seguridad, indemnización o evacuación.
4. **Reporte ciudadano futuro:** capturar evidencia desde lugar seguro → declarar fecha/lugar → revisión/privacidad → estado «pendiente de verificar» o «verificado» con procedencia.

## Modelo conceptual / APIs candidatas

- `GET /v1/rain/observed?lat&lon&window=1h|6h|24h|72h` (solo ventanas soportadas)
- `GET /v1/rain/forecast?lat&lon&horizon=24|48|72`
- `GET /v1/terrain/context?lat&lon` (capas y limitaciones)
- `GET /v1/events?bbox&from&to&type` (registro auditado)
- `GET /v1/preparedness?hazard=landslide` (contenido validado/versionado)
- `GET /v1/sources` (licencias, actualización, resolución y cobertura)

Estructura mínima por indicador: `value`, `unit`, `source_id`, `observed_at`, `issued_at`, `retrieved_at`, `spatial_resolution`, `coverage`, `quality_flag`, `limitations`.

## Pruebas de aceptación

- Si falla la fuente, mensaje «No hay datos recientes»; nunca «sector seguro».
- Diferenciar precipitación pasada de pronóstico y unidades de mm frente a mm/h.
- Al cambiar ubicación, no reutilizar silenciosamente datos de otra celda o comuna.
- Eventos sin localización validada se muestran a nivel geográfico aproximado y con etiqueta visible.
- Capas sin licencia o disponibilidad confirmada quedan deshabilitadas, no simuladas.
- No generar avisos de evacuación ni un índice numérico de riesgo no calibrado.
- Pruebas móviles, teclado, lectores de pantalla, tiempos de actualización y mensajes de fallo.

## Fuentes candidatas y verificación pendiente

- SENAPRED: https://www.senapred.cl/
- SERNAGEOMIN: https://portalgeomin.sernageomin.cl/
- DMC: https://www.meteochile.gob.cl/
- DGA: https://dga.mop.gob.cl/
- NASA IMERG: https://gpm.nasa.gov/data/imerg
- NASA LHASA: https://github.com/nasa/lhasa

Antes de integrar: documentar cobertura efectiva, fecha, granularidad, términos de uso/API, licencia de redistribución y capacidad de actualizaciones automáticas. Evitar scraping no permitido.

## Criterios de avance

P0: capas auténticas verificadas, fichas explicables, fechas visibles y al menos un conjunto de eventos documentados auditado. P1: pruebas de comprensión/seguridad con usuarios y protección de datos. P2: evaluación retrospectiva rigurosa y revisión externa antes de notificaciones predictivas.

**Nota:** el roadmap es una propuesta de desarrollo y no constituye una alerta meteorológica vigente.
