# Pipelines de ingesta (ETL)

Ningún pipeline de este directorio corre automáticamente en el MVP actual: el backend
(`services/api`) consulta Open-Meteo directamente en tiempo de solicitud porque es la única
fuente `approved` (ver `docs/FUENTES_ESTADO.md`). Este directorio queda como scaffolding para
cuando otras fuentes (IMERG, DEM, DGA, SERNAGEOMIN) pasen sus respectivos gates G0/G1.

- `imerg/` — importador de investigación para NASA GPM IMERG. **No activado**: requiere cuenta
  NASA Earthdata y verificación de licencia/latencia antes de cualquier ingesta, incluso en modo
  investigación (ver `docs/AUDITORIA_MVP_2026-10-14.md` entregable 4).
- `sernageomin_unab_catalog/fetch_and_filter.py` — **único script de este directorio que sí se
  ejecutó** (manualmente, no en vivo): consulta un catastro de terceros de remociones en masa
  (Universidad Andrés Bello, vía ArcGIS Online, licencia `pending`) y genera
  `services/api/app/data/sernageomin_unab_catalog_sjm.json`, consumido por
  `app/events_data.py` con `verification_status="pending_review"`. Ver `docs/DECISIONES.md` para
  el detalle de la investigación y las salvedades de licencia.

Reglas para cualquier pipeline futuro en este directorio:

1. No ingerir una fuente cuya licencia esté `pending` o `blocked` en `services/api/app/sources.py`.
2. Todo dato debe conservar unidades originales, fecha de observación/emisión y procedencia.
3. Ningún valor inventado ante hueco de datos: `null` explícito.
4. Pruebas de cobertura geográfica y manejo de celdas vacías antes de habilitar.
