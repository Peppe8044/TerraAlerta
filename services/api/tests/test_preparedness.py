from __future__ import annotations


def test_preparedness_landslide_checklist_has_attribution_and_no_evacuation_routes(client):
    response = client.get("/v1/preparedness", params={"hazard": "landslide"})
    assert response.status_code == 200
    body = response.json()
    assert body["official_url"] == "https://www.senapred.cl/"
    assert body["source_attribution"]
    assert body["version"]
    joined_text = " ".join(item["text"] for item in body["items"]).lower()
    # No debe prescribir rutas de evacuación propias; debe derivar a la autoridad.
    assert "ruta de evacuación" not in joined_text or "autoridad" in joined_text


def test_preparedness_unknown_hazard_returns_404(client):
    response = client.get("/v1/preparedness", params={"hazard": "unknown_hazard"})
    assert response.status_code == 404
