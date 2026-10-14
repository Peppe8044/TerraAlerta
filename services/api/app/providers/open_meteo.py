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


def _validate_hourly_series(hourly: dict[str, Any], expected_length: int) -> tuple[list[str], list[float]]:
    """Valida que la serie horaria venga completa antes de sumarla.

    Lanza `ProviderError` si faltan horas, si el arreglo viene vacío o si
    todos los valores son `null`. Nunca se trata un hueco de datos como 0 mm
    (ver hallazgo de revisión en PR #1: un arreglo vacío/`null` no debe
    reportarse como `quality_flag="real"` con valor 0).
    """
    times: list[str] = hourly.get("time", [])
    raw_values: list[float | None] = hourly.get("precipitation", [])

    if not times or not raw_values or len(raw_values) < expected_length:
        raise ProviderError(
            f"Serie horaria incompleta: se esperaban {expected_length} horas, llegaron {len(raw_values)}."
        )
    if all(v is None for v in raw_values):
        raise ProviderError("Serie horaria sin datos numéricos (todos los valores son null).")

    # Tratar cada hueco puntual como 0 solo cuando el resto de la serie es real;
    # si llegó al menos un valor no nulo, los huecos puntuales son aceptables
    # dentro de la ventana (p. ej. un sensor del modelo con un paso faltante).
    values: list[float] = [v for v in raw_values if v is not None]
    return times, values


def get_forecast(lat: float, lon: float, horizon: int) -> dict[str, Any]:
    """Pronóstico acumulado de precipitación a 24/48/72 h desde Open-Meteo.

    Usa `forecast_hours` (alineado a la hora actual), no `forecast_days`
    (alineado a medianoche): con `forecast_days` una consulta hecha a media
    tarde sumaría sobre todo horas ya transcurridas del día en curso en vez
    de las próximas `horizon` horas (hallazgo de revisión en PR #1).

    Lanza `ProviderError` si la fuente falla, si la serie viene incompleta o
    si `horizon` no es uno de los valores soportados (este último vía
    `ValueError`, error de uso, no de proveedor).
    """
    if horizon not in ALLOWED_FORECAST_HORIZONS:
        raise ValueError(f"Horizonte no soportado: {horizon}. Use uno de {ALLOWED_FORECAST_HORIZONS}.")

    settings = get_settings()
    payload = _fetch_json(
        f"{settings.open_meteo_base_url}/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation",
            "forecast_hours": horizon,
            "timezone": settings.timezone,
        },
        timeout=settings.open_meteo_timeout_seconds,
    )

    times, values = _validate_hourly_series(payload.get("hourly", {}), expected_length=horizon)
    accumulated = sum(values)

    return {
        "value": round(accumulated, 2),
        "unit": "mm",
        "issued_at": _retrieved_at_now(),
        "observed_at": None,
        "retrieved_at": _retrieved_at_now(),
        "coverage_start": times[0],
        "coverage_end": times[-1],
        "model_elevation_m": payload.get("elevation"),
    }


def get_recent_precipitation(lat: float, lon: float, window_hours: int) -> dict[str, Any]:
    """Precipitación reciente (ventana pasada) vía Open-Meteo `past_hours`.

    Usa `past_hours`/`forecast_hours=0` (ventana terminada justo antes de la
    hora en curso), no `past_days` (alineado a medianoche): con `past_days`
    una consulta de "últimas 6 horas" hecha a media tarde devolvía
    medianoche-06:00 de hoy, no las 6 horas inmediatamente anteriores
    (hallazgo de revisión en PR #1).

    Importante: esto es un modelo numérico reanalizado, NO una observación
    de pluviómetro ni un producto satelital IMERG. Se etiqueta así en
    `limitations` por quien consuma esta función.
    """
    if window_hours not in ALLOWED_OBSERVED_WINDOWS:
        raise ValueError(f"Ventana no soportada: {window_hours}. Use una de {ALLOWED_OBSERVED_WINDOWS}.")

    settings = get_settings()
    payload = _fetch_json(
        f"{settings.open_meteo_base_url}/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation",
            "past_hours": window_hours,
            "forecast_hours": 0,
            "timezone": settings.timezone,
        },
        timeout=settings.open_meteo_timeout_seconds,
    )

    times, values = _validate_hourly_series(payload.get("hourly", {}), expected_length=window_hours)
    accumulated = sum(values)

    return {
        "value": round(accumulated, 2),
        "unit": "mm",
        "observed_at": times[-1],
        "retrieved_at": _retrieved_at_now(),
        "coverage_start": times[0],
        "coverage_end": times[-1],
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
