"""Verificación de cobertura geográfica para el MVP (San José de Maipo).

El bounding box es una aproximación operativa para el piloto, **no** un
límite administrativo oficial. Antes de ampliar cobertura, reemplazar por
la geometría oficial de la comuna (INE/BCN) — ver docs/DECISIONES.md.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings, get_settings


@dataclass(frozen=True)
class CoverageResult:
    in_coverage: bool
    reason: str | None = None


def check_coverage(lat: float, lon: float, settings: Settings | None = None) -> CoverageResult:
    settings = settings or get_settings()

    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
        return CoverageResult(False, "Coordenadas fuera de rango válido (lat/lon).")

    inside = (
        settings.pilot_bbox_min_lat <= lat <= settings.pilot_bbox_max_lat
        and settings.pilot_bbox_min_lon <= lon <= settings.pilot_bbox_max_lon
    )
    if not inside:
        return CoverageResult(
            False,
            "Punto fuera de la zona piloto (San José de Maipo). El MVP no cubre esta ubicación.",
        )
    return CoverageResult(True, None)
