from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.providers import open_meteo

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "open_meteo_forecast_synthetic.json"

# Fuera de la zona piloto (Punta Arenas) — debe rechazarse en todos los
# endpoints que reciben lat/lon, no solo en /v1/locations/summary.
OUT_OF_COVERAGE_PARAMS = {"lat": -53.1638, "lon": -70.9171}


@pytest.fixture
def synthetic_forecast_payload():
    with open(FIXTURE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def patch_open_meteo(monkeypatch, synthetic_forecast_payload):
    def fake_fetch_json(url, params, timeout):
        return synthetic_forecast_payload

    monkeypatch.setattr(open_meteo, "_fetch_json", fake_fetch_json)


def test_forecast_endpoint_with_synthetic_fixture(client, patch_open_meteo):
    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    assert response.status_code == 200
    body = response.json()
    assert body["unit"] == "mm"
    assert body["source_id"] == "open_meteo_forecast"
    assert body["quality_flag"] == "real"
    assert body["value"] is not None
    assert body["limitations"]


def test_forecast_rejects_invalid_horizon(client):
    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 36})
    assert response.status_code == 422


def test_forecast_rejects_point_outside_pilot_coverage(client, patch_open_meteo):
    """Hallazgo de revisión PR #1: este endpoint no aplicaba el guard de cobertura."""
    response = client.get(
        "/v1/precipitation/forecast", params={**OUT_OF_COVERAGE_PARAMS, "horizon": 24}
    )
    assert response.status_code == 422
    assert "zona piloto" in response.json()["detail"]


def test_observed_endpoint_with_synthetic_fixture(client, patch_open_meteo):
    response = client.get("/v1/rain/observed", params={"lat": -33.6378, "lon": -70.3539, "window": 6})
    assert response.status_code == 200
    body = response.json()
    assert body["unit"] == "mm"
    assert any("no" in lim.lower() for lim in body["limitations"])  # debe advertir que no es IMERG/estación


def test_observed_rejects_invalid_window(client):
    response = client.get("/v1/rain/observed", params={"lat": -33.6378, "lon": -70.3539, "window": 48})
    assert response.status_code == 422


def test_observed_rejects_point_outside_pilot_coverage(client, patch_open_meteo):
    """Hallazgo de revisión PR #1: este endpoint no aplicaba el guard de cobertura."""
    response = client.get("/v1/rain/observed", params={**OUT_OF_COVERAGE_PARAMS, "window": 6})
    assert response.status_code == 422
    assert "zona piloto" in response.json()["detail"]


def test_forecast_provider_unavailable_returns_unavailable_flag(client, monkeypatch):
    def failing_fetch(url, params, timeout):
        raise open_meteo.ProviderError("timeout simulado")

    monkeypatch.setattr(open_meteo, "_fetch_json", failing_fetch)

    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    assert response.status_code == 200
    body = response.json()
    assert body["quality_flag"] == "unavailable"
    assert body["value"] is None


def test_forecast_with_empty_series_is_unavailable_not_zero(client, monkeypatch):
    """Hallazgo de revisión PR #1: un arreglo vacío/null NUNCA debe reportarse como 0 mm 'real'."""

    def empty_series_fetch(url, params, timeout):
        return {"hourly": {"time": [], "precipitation": []}}

    monkeypatch.setattr(open_meteo, "_fetch_json", empty_series_fetch)

    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    body = response.json()
    assert body["quality_flag"] == "unavailable"
    assert body["value"] is None


def test_forecast_with_all_null_series_is_unavailable_not_zero(client, monkeypatch):
    def all_null_fetch(url, params, timeout):
        return {
            "hourly": {
                "time": [f"2026-10-14T{h:02d}:00" for h in range(24)],
                "precipitation": [None] * 24,
            }
        }

    monkeypatch.setattr(open_meteo, "_fetch_json", all_null_fetch)

    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    body = response.json()
    assert body["quality_flag"] == "unavailable"
    assert body["value"] is None


def test_forecast_with_short_series_is_unavailable_not_truncated(client, monkeypatch):
    """Una serie más corta que el horizonte pedido no debe sumarse a medias y presentarse como completa."""

    def short_series_fetch(url, params, timeout):
        return {
            "hourly": {
                "time": [f"2026-10-14T{h:02d}:00" for h in range(10)],
                "precipitation": [1.0] * 10,
            }
        }

    monkeypatch.setattr(open_meteo, "_fetch_json", short_series_fetch)

    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    body = response.json()
    assert body["quality_flag"] == "unavailable"
    assert body["value"] is None
