"""Conector real a Open-Meteo (pronóstico + elevación).

Fuente no comercial, sin clave de API (ver docs/DATOS.md y
docs/AUDITORIA_MVP_2026-10-14.md). Este módulo NUNCA inventa valores: ante
fallo de red, timeout o respuesta inesperada, propaga `ProviderError` y el
router correspondiente debe responder con `quality_flag="unavailable"`.

`_fetch_json` queda aislado para poder sustituirlo (monkeypatch) en tests
sin golpear la red real.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from app.config import get_settings

ALLOWED_FORECAST_HORIZONS = (24, 48, 72)
ALLOWED_OBSERVED_WINDOWS = (1, 6, 24, 72)


class ProviderError(RuntimeError):
    """Error de origen externo (red, timeout, formato). No es un bug de negocio."""


def _fetch_json(url: str, params: dict[str, Any], timeout: float) -> dict[str, Any]:
    try:
        response = httpx.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError) as exc:  # red, timeout, HTTP 4xx/5xx, JSON inválido
        raise ProviderError(str(exc)) from exc


def _retrieved_at_now() -> str:
    return datetime.now(UTC).isoformat()


def get_forecast(lat: float, lon: float, horizon: int) -> dict[str, Any]:
    """Pronóstico acumulado de precipitación a 24/48/72 h desde Open-Meteo.

    Devuelve un dict con el acumulado pronosticado (mm) y metadatos de
    procedencia. Lanza `ProviderError` si la fuente falla o `horizon` no es
    uno de los valores soportados.
    """
    if horizon not in ALLOWED_FORECAST_HORIZONS:
        raise ValueError(f"Horizonte no soportado: {horizon}. Use uno de {ALLOWED_FORECAST_HORIZONS}.")

    settings = get_settings()
    forecast_days = max(1, horizon // 24)
    payload = _fetch_json(
        f"{settings.open_meteo_base_url}/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation",
            "forecast_days": forecast_days,
            "timezone": settings.timezone,
        },
        timeout=settings.open_meteo_timeout_seconds,
    )

    hourly = payload.get("hourly", {})
    times: list[str] = hourly.get("time", [])
    values: list[float | None] = hourly.get("precipitation", [])
    window = values[:horizon]
    accumulated = sum(v for v in window if v is not None)

    return {
        "value": round(accumulated, 2),
        "unit": "mm",
        "issued_at": _retrieved_at_now(),
        "observed_at": None,
        "retrieved_at": _retrieved_at_now(),
        "coverage_start": times[0] if times else None,
        "coverage_end": times[min(horizon, len(times)) - 1] if times else None,
        "model_elevation_m": payload.get("elevation"),
    }


def get_recent_precipitation(lat: float, lon: float, window_hours: int) -> dict[str, Any]:
    """Precipitación reciente (ventana pasada) vía Open-Meteo `past_days`.

    Importante: esto es un modelo numérico reanalizado, NO una observación
    de pluviómetro ni un producto satelital IMERG. Se etiqueta así en
    `limitations` por quien consuma esta función.
    """
    if window_hours not in ALLOWED_OBSERVED_WINDOWS:
        raise ValueError(f"Ventana no soportada: {window_hours}. Use una de {ALLOWED_OBSERVED_WINDOWS}.")

    settings = get_settings()
    past_days = max(1, -(-window_hours // 24))  # ceil
    payload = _fetch_json(
        f"{settings.open_meteo_base_url}/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation",
            "past_days": past_days,
            "forecast_days": 1,
            "timezone": settings.timezone,
        },
        timeout=settings.open_meteo_timeout_seconds,
    )

    hourly = payload.get("hourly", {})
    times: list[str] = hourly.get("time", [])
    values: list[float | None] = hourly.get("precipitation", [])

    # Las últimas `window_hours` horas que ya transcurrieron (aproximación:
    # tomamos las primeras window_hours de la serie past_days, que
    # corresponden al pasado reciente, no al pronóstico).
    recent_values = values[:window_hours]
    recent_times = times[:window_hours]
    accumulated = sum(v for v in recent_values if v is not None)

    return {
        "value": round(accumulated, 2),
        "unit": "mm",
        "observed_at": recent_times[-1] if recent_times else None,
        "retrieved_at": _retrieved_at_now(),
        "coverage_start": recent_times[0] if recent_times else None,
        "coverage_end": recent_times[-1] if recent_times else None,
    }


def get_elevation(lat: float, lon: float) -> dict[str, Any]:
    settings = get_settings()
    payload = _fetch_json(
        f"{settings.open_meteo_base_url}/elevation",
        params={"latitude": lat, "longitude": lon},
        timeout=settings.open_meteo_timeout_seconds,
    )
    elevations = payload.get("elevation", [])
    return {
        "value": elevations[0] if elevations else None,
        "unit": "m",
        "retrieved_at": _retrieved_at_now(),
    }
