# Arquitectura MVP

```
  [IMERG / pronóstico / DEM / capas Chile]
                  |
       [pipelines Python ETL]
                  |
  [PostgreSQL + PostGIS + almacenamiento de rasters]
                  |
          [FastAPI /v1]
                  |
       [Next.js + MapLibre]
                  |
       [móvil como web responsiva]
```

## Contratos API propuestos

- `GET /health` -> estado servicio, sin afirmar frescura de fuentes.
- `GET /v1/sources` -> datasets, licencia y última actualización.
- `GET /v1/locations/summary?lat=&lon=` -> indicadores disponibles con fecha, escala, origen y limitaciones. Rechazar puntos fuera de cobertura.
- `GET /v1/precipitation/forecast?lat=&lon=&horizon=24|48|72` -> acumulados pronosticados y ciclo del modelo.
- `GET /v1/terrain/profile?lat=&lon=` -> altitud/pendiente con resolución y procedencia.

## Ejemplo conceptual

```json
{
  "location": {"lat": -33.6, "lon": -70.35},
  "experimental": true,
  "status": "partial_data",
  "indicators": [
    {"name": "forecast_rain_24h", "value": null, "unit": "mm", "source": "pending", "observed_at": null}
  ],
  "limitations": ["Esta información no predice daños en una propiedad."],
  "official_alerts_url": "https://www.senapred.cl/"
}
```

**Valores y coordenadas de ejemplo no constituyen observaciones reales.**

## Tecnología

Python 3.12+, FastAPI, Pydantic, pandas, Xarray, Rasterio, GeoPandas, PostgreSQL + PostGIS, Next.js, TypeScript, MapLibre, Docker Compose, pytest. MinIO opcional solo si hace falta almacenar GeoTIFF; evitar complejidad prematura.

## Seguridad y operación

Rate limits, caché de resultados, geocodificación bajo condiciones claras, no guardar ubicación personal por defecto; registro de errores sin coordenadas privadas, actualización horaria parametrizable con alertas por ETL fallido, health checks y copia de respaldo.
