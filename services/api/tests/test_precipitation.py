from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.providers import open_meteo

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "open_meteo_forecast_synthetic.json"


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


def test_observed_endpoint_with_synthetic_fixture(client, patch_open_meteo):
    response = client.get("/v1/rain/observed", params={"lat": -33.6378, "lon": -70.3539, "window": 6})
    assert response.status_code == 200
    body = response.json()
    assert body["unit"] == "mm"
    assert any("no" in lim.lower() for lim in body["limitations"])  # debe advertir que no es IMERG/estación


def test_observed_rejects_invalid_window(client):
    response = client.get("/v1/rain/observed", params={"lat": -33.6378, "lon": -70.3539, "window": 48})
    assert response.status_code == 422


def test_forecast_provider_unavailable_returns_unavailable_flag(client, monkeypatch):
    def failing_fetch(url, params, timeout):
        raise open_meteo.ProviderError("timeout simulado")

    monkeypatch.setattr(open_meteo, "_fetch_json", failing_fetch)

    response = client.get("/v1/precipitation/forecast", params={"lat": -33.6378, "lon": -70.3539, "horizon": 24})
    assert response.status_code == 200
    body = response.json()
    assert body["quality_flag"] == "unavailable"
    assert body["value"] is None
