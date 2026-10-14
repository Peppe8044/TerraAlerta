from __future__ import annotations

from app.providers import open_meteo


def test_location_summary_rejects_point_outside_pilot_coverage(client):
    response = client.get("/v1/locations/summary", params={"lat": -53.1638, "lon": -70.9171})
    assert response.status_code == 422
    assert "zona piloto" in response.json()["detail"]


def test_location_summary_returns_indicators_with_full_traceability(client, monkeypatch):
    def fake_fetch_json(url, params, timeout):
        if "elevation" in url:
            return {"elevation": [957.0]}
        return {
            "elevation": 957.0,
            "hourly": {
                "time": [f"2026-10-14T{h:02d}:00" for h in range(24)],
                "precipitation": [0.0] * 24,
            },
        }

    monkeypatch.setattr(open_meteo, "_fetch_json", fake_fetch_json)

    response = client.get("/v1/locations/summary", params={"lat": -33.6378, "lon": -70.3539})
    assert response.status_code == 200
    body = response.json()

    assert body["experimental"] is True
    assert body["status"] in ("sufficient_data", "partial_data", "unavailable")
    assert body["official_alerts_url"] == "https://www.senapred.cl/"
    assert len(body["limitations"]) >= 1

    for indicator in body["indicators"]:
        assert indicator["source_id"]
        assert indicator["retrieved_at"]
        assert indicator["spatial_resolution"]
        assert indicator["coverage"]
        assert "limitations" in indicator


def test_location_summary_never_exposes_unapproved_source_as_real(client, monkeypatch):
    def fake_fetch_json(url, params, timeout):
        if "elevation" in url:
            return {"elevation": [957.0]}
        return {"hourly": {"time": [], "precipitation": []}}

    monkeypatch.setattr(open_meteo, "_fetch_json", fake_fetch_json)

    response = client.get("/v1/locations/summary", params={"lat": -33.6378, "lon": -70.3539})
    body = response.json()
    allowed_real_sources = {"open_meteo_forecast", "open_meteo_elevation"}
    for indicator in body["indicators"]:
        if indicator["quality_flag"] == "real":
            assert indicator["source_id"] in allowed_real_sources
