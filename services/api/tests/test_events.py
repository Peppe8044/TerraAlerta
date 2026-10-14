from __future__ import annotations


def test_events_endpoint_returns_only_officially_sourced_entries(client):
    """Gate: no simular aluviones reales (docs/AUDITORIA_MVP_2026-10-14.md).

    Cada evento debe traer una fuente oficial citable (URL verificable) y
    declarar explícitamente su nivel de certeza de localización y su
    estado de verificación — nunca presentarse como un hecho sin matices.
    """
    response = client.get("/v1/events")
    assert response.status_code == 200
    body = response.json()

    assert len(body["events"]) >= 1
    assert "verificad" in body["message"].lower()

    for event in body["events"]:
        assert event["source"].startswith(("SERNAGEOMIN", "SENAPRED", "DGA", "DMC"))
        assert "http" in event["source"]
        assert event["location_certainty"] in ("verified", "approximate", "unverified_candidate")
        assert event["verification_status"] in ("verified", "pending_review")
        assert event["hazard_type"] in ("aluvion", "remocion_en_masa", "inundacion")


def test_events_does_not_include_unverified_las_condes_2026_candidate(client):
    """docs/ALUVIONES_Y_PREVENCION.md: el candidato de Las Condes 2026 NO debe incorporarse
    sin fuente oficial/localización verificada."""
    response = client.get("/v1/events")
    body = response.json()
    event_ids = [event["id"] for event in body["events"]]
    assert not any("las-condes" in event_id.lower() for event_id in event_ids)
    assert not any("2026" in event_id for event_id in event_ids)
