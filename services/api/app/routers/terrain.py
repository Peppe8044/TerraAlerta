from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query

from app.coverage import check_coverage
from app.providers import open_meteo
from app.providers.open_meteo import ProviderError
from app.schemas import Indicator

router = APIRouter()


@router.get("/v1/terrain/profile", response_model=list[Indicator])
def terrain_profile(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
) -> list[Indicator]:
    """Perfil de terreno disponible en el MVP.

    Solo entrega elevación puntual (real, vía Open-Meteo/Copernicus DEM
    GLO-90). La pendiente requiere procesar un DEM con licencia verificada
    (Copernicus GLO-30/GLO-90) — ver docs/AUDITORIA_MVP_2026-10-14.md — y
    permanece `unavailable` hasta completar ese gate.
    """
    coverage = check_coverage(lat, lon)
    if not coverage.in_coverage:
        raise HTTPException(status_code=422, detail=coverage.reason)

    retrieved_at = datetime.now(UTC).isoformat()

    try:
        elevation = open_meteo.get_elevation(lat, lon)
        elevation_indicator = Indicator(
            name="elevation",
            value=elevation["value"],
            unit=elevation["unit"],
            source_id="open_meteo_elevation",
            observed_at=None,
            retrieved_at=elevation["retrieved_at"],
            spatial_resolution="~90 m (Copernicus DEM GLO-90)",
            coverage="San José de Maipo (piloto)",
            quality_flag="real",
            limitations=[
                "Modelo de superficie, no levantamiento detallado del terreno.",
                "No implica seguridad ni ausencia de riesgo en el punto exacto.",
            ],
        )
    except ProviderError:
        elevation_indicator = Indicator(
            name="elevation",
            value=None,
            unit="m",
            source_id="open_meteo_elevation",
            retrieved_at=retrieved_at,
            spatial_resolution="~90 m (Copernicus DEM GLO-90)",
            coverage="San José de Maipo (piloto)",
            quality_flag="unavailable",
            limitations=["No hay datos recientes del proveedor de elevación."],
        )

    slope_indicator = Indicator(
        name="slope",
        value=None,
        unit="deg",
        source_id="copernicus_dem",
        retrieved_at=retrieved_at,
        spatial_resolution="pendiente",
        coverage="San José de Maipo (piloto)",
        quality_flag="unavailable",
        limitations=[
            "Pendiente no disponible aún: requiere verificar licencia y resolución del DEM (gate G0/G3).",
        ],
    )

    return [elevation_indicator, slope_indicator]
