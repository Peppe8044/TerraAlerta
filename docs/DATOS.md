# Inventario y gobernanza de datos

| Fuente | Uso | Precaución | Acceso |
|---|---|---|---|
| NASA GPM IMERG | Precipitación histórica y reciente | Resolución aprox. 0,1°; el producto Early es diferido. No representa lluvia exacta sobre una parcela | https://gpm.nasa.gov/data/imerg |
| NASA LHASA | Referencia externa para deslizamientos | ~1 km diario; disponibilidad operativa variable; el repositorio no ofrece un proceso directo para reentrenar el modelo global | https://github.com/nasa/lhasa |
| Copernicus DEM GLO-30/GLO-90 | Relieve / pendiente | Es un modelo de superficie, no levantamiento detallado del terreno. Acceso GLO-30 sujeto a registro CCM desde julio 2026; atribución y licencias | https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM.html |
| Open-Meteo | Pronóstico en etapa no comercial | Revisar términos; API gratuita no se debe asumir habilitada para uso comercial | https://open-meteo.com/en/terms |
| DMC / DGA / IDE Chile | Observaciones y capas locales | Verificar API disponible, derechos de reutilización, cobertura, fechas y calidad por estación/capa | https://www.meteochile.gob.cl/ ; https://dga.mop.gob.cl/ ; https://www.ide.cl/ |
| Copernicus GloFAS | Referencia de crecidas fluviales de mayor escala | No equivale a mapa de inundación de parcela | https://global-flood.emergency.copernicus.eu/ |
| Google Flood Hub | Comparación externa | Su API requiere autorización; no depender de ella en el MVP | https://sites.research.google/gr/floodforecasting/ |

## Reglas obligatorias

- Registro por fuente: `dataset`, `url`, `license_status` (`verified`/`pending`/`restricted`), `retrieved_at`, `observed_at`, `coverage_geometry`, `resolution`, `latency`, `version`.
- No procesar una fuente cuya licencia esté pendiente para redistribución pública; habilitar conectores exclusivamente cuando proceda.
- Separar DEM estático, lluvia observada y pronóstico; no sumar valores si unidades o ventanas temporales difieren.
- Conservar metadatos de reproyección, fechas UTC y horario local America/Santiago en interfaz.
- Incluir test de cobertura geográfica de Santiago y manejo explícito de celdas vacías.
- Verificar nominalmente las licencias y condiciones actuales antes de comercializar, copiar redistribuir, entrenar o publicar derivados.
