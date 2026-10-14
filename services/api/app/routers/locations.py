from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query

from app.coverage import check_coverage
from app.providers import open_meteo
from app.providers.open_meteo import ProviderError
from app.schemas import DataStatus, Indicator, LocationSummary

router = APIRouter()


def _forecast_indicator(lat: float, lon: float, horizon: int) -> Indicator:
    try:
        result = open_meteo.get_forecast(lat, lon, horizon)
        return Indicator(
            name=f"forecast_rain_{horizon}h",
            value=result["value"],
            unit=result["unit"],
            source_id="open_meteo_forecast",
            issued_at=result["issued_at"],
            retrieved_at=result["retrieved_at"],
            spatial_resolution="modelo numérico (no estación puntual)",
            coverage=f"{result.get('coverage_start')} a {result.get('coverage_end')}",
            quality_flag="real",
            limitations=["Pronóstico de modelo numérico; no garantiza precipitación real futura."],
        )
    except ProviderError:
        return Indicator(
            name=f"forecast_rain_{horizon}h",
            value=None,
            unit="mm",
            source_id="open_meteo_forecast",
            retrieved_at=datetime.now(UTC).isoformat(),
            spatial_resolution="modelo numérico",
            coverage="San José de Maipo (piloto)",
            quality_flag="unavailable",
            limitations=["No hay datos recientes del proveedor de pronóstico."],
        )


def _elevation_indicator(lat: float, lon: float) -> Indicator:
    try:
        elevation = open_meteo.get_elevation(lat, lon)
        return Indicator(
            name="elevation",
            value=elevation["value"],
            unit=elevation["unit"],
            source_id="open_meteo_elevation",
            retrieved_at=elevation["retrieved_at"],
            spatial_resolution="~90 m (Copernicus DEM GLO-90)",
            coverage="San José de Maipo (piloto)",
            quality_flag="real",
            limitations=["Modelo de superficie; no implica seguridad en el punto exacto."],
        )
    except ProviderError:
        return Indicator(
            name="elevation",
            value=None,
            unit="m",
            source_id="open_meteo_elevation",
            retrieved_at=datetime.now(UTC).isoformat(),
            spatial_resolution="~90 m",
            coverage="San José de Maipo (piloto)",
            quality_flag="unavailable",
            limitations=["No hay datos recientes del proveedor de elevación."],
        )


def _overall_status(indicators: list[Indicator]) -> DataStatus:
    real_count = sum(1 for i in indicators if i.quality_flag == "real")
    if real_count == len(indicators) and real_count > 0:
        return "sufficient_data"
    if real_count > 0:
        return "partial_data"
    return "unavailable"


@router.get("/v1/locations/summary", response_model=LocationSummary)
def location_summary(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
) -> LocationSummary:
    coverage = check_coverage(lat, lon)
    if not coverage.in_coverage:
        raise HTTPException(status_code=422, detail=coverage.reason)

    indicators = [
        _forecast_indicator(lat, lon, 24),
        _forecast_indicator(lat, lon, 72),
        _elevation_indicator(lat, lon),
    ]

    return LocationSummary(
        location={"lat": lat, "lon": lon},
        experimental=True,
        status=_overall_status(indicators),
        indicators=indicators,
        limitations=[
            "Esta información no predice daños en una propiedad específica.",
            "No sustituye a SENAPRED ni constituye una alerta oficial vigente.",
            "La pendiente del terreno y las capas de amenaza aún no están disponibles en este MVP.",
        ],
    )
