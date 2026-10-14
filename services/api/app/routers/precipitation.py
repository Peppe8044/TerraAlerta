from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query

from app.providers import open_meteo
from app.providers.open_meteo import ProviderError
from app.schemas import Indicator

router = APIRouter()


@router.get("/v1/precipitation/forecast", response_model=Indicator)
def forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    horizon: int = Query(..., description="Horizonte en horas: 24, 48 o 72"),
) -> Indicator:
    if horizon not in open_meteo.ALLOWED_FORECAST_HORIZONS:
        raise HTTPException(status_code=422, detail="horizon debe ser 24, 48 o 72")

    try:
        result = open_meteo.get_forecast(lat, lon, horizon)
    except ProviderError:
        return Indicator(
            name=f"forecast_rain_{horizon}h",
            value=None,
            unit="mm",
            source_id="open_meteo_forecast",
            retrieved_at=datetime.now(UTC).isoformat(),
            spatial_resolution="modelo numérico (variable según celda)",
            coverage="San José de Maipo (piloto)",
            quality_flag="unavailable",
            limitations=["No hay datos recientes del proveedor de pronóstico."],
        )

    return Indicator(
        name=f"forecast_rain_{horizon}h",
        value=result["value"],
        unit=result["unit"],
        source_id="open_meteo_forecast",
        issued_at=result["issued_at"],
        observed_at=None,
        retrieved_at=result["retrieved_at"],
        spatial_resolution="modelo numérico (no estación puntual)",
        coverage=f"{result.get('coverage_start')} a {result.get('coverage_end')}",
        quality_flag="real",
        limitations=[
            "Pronóstico de modelo numérico, no una garantía de precipitación real futura.",
            "No predice daños ni inundación en una vivienda específica.",
        ],
    )


@router.get("/v1/rain/observed", response_model=Indicator)
def observed(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    window: int = Query(..., description="Ventana en horas: 1, 6, 24 o 72"),
) -> Indicator:
    if window not in open_meteo.ALLOWED_OBSERVED_WINDOWS:
        raise HTTPException(status_code=422, detail="window debe ser 1, 6, 24 o 72")

    try:
        result = open_meteo.get_recent_precipitation(lat, lon, window)
    except ProviderError:
        return Indicator(
            name=f"recent_rain_{window}h",
            value=None,
            unit="mm",
            source_id="open_meteo_forecast",
            retrieved_at=datetime.now(UTC).isoformat(),
            spatial_resolution="modelo numérico (variable según celda)",
            coverage="San José de Maipo (piloto)",
            quality_flag="unavailable",
            limitations=["No hay datos recientes disponibles."],
        )

    return Indicator(
        name=f"recent_rain_{window}h",
        value=result["value"],
        unit=result["unit"],
        source_id="open_meteo_forecast",
        observed_at=result["observed_at"],
        retrieved_at=result["retrieved_at"],
        spatial_resolution="modelo numérico (no estación puntual)",
        coverage=f"{result.get('coverage_start')} a {result.get('coverage_end')}",
        quality_flag="real",
        limitations=[
            "Estimación de modelo numérico reanalizado, no observación de pluviómetro ni producto satelital IMERG.",
            "No representa lluvia exacta sobre una parcela.",
        ],
    )
