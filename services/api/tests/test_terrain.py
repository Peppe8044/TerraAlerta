from __future__ import annotations

from app.providers import open_meteo


def test_terrain_profile_returns_elevation_and_unavailable_slope(client, monkeypatch):
    def fake_fetch_json(url, params, timeout):
        return {"elevation": [957.0]}

    monkeypatch.setattr(open_meteo, "_fetch_json", fake_fetch_json)

    response = client.get("/v1/terrain/profile", params={"lat": -33.6378, "lon": -70.3539})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2

    by_name = {ind["name"]: ind for ind in body}
    assert by_name["elevation"]["value"] == 957.0
    assert by_name["elevation"]["quality_flag"] == "real"

    # La pendiente NO debe inventarse: debe quedar explícitamente no disponible.
    assert by_name["slope"]["value"] is None
    assert by_name["slope"]["quality_flag"] == "unavailable"


def test_terrain_profile_handles_provider_failure_without_inventing_values(client, monkeypatch):
    def failing_fetch(url, params, timeout):
        raise open_meteo.ProviderError("timeout simulado")

    monkeypatch.setattr(open_meteo, "_fetch_json", failing_fetch)

    response = client.get("/v1/terrain/profile", params={"lat": -33.6378, "lon": -70.3539})
    assert response.status_code == 200
    body = response.json()
    by_name = {ind["name"]: ind for ind in body}
    assert by_name["elevation"]["value"] is None
    assert by_name["elevation"]["quality_flag"] == "unavailable"
