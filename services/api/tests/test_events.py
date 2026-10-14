from __future__ import annotations

from app import events_data
from app.schemas import EventRecord

# Único evento permitido a tener verification_status="verified": fue
# investigado a mano contra una fuente primaria (ver app/events_data.py).
# Cualquier otro "verified" indicaría que un lote importado masivamente
# se marcó como verificado sin la investigación individual que eso exige.
_ALLOWED_VERIFIED_IDS = {"sjm-2017-02-quebrada-san-jose"}


def test_events_endpoint_returns_only_officially_sourced_entries(client):
    """Gate: no simular aluviones reales (docs/AUDITORIA_MVP_2026-10-14.md).

    Cada evento debe traer una fuente citable que mencione SERNAGEOMIN (el
    organismo que documenta el informe original) y declarar explícitamente
    su nivel de certeza de localización y su estado de verificación — nunca
    presentarse como un hecho sin matices.
    """
    response = client.get("/v1/events")
    assert response.status_code == 200
    body = response.json()

    assert len(body["events"]) >= 1
    assert "verificad" in body["message"].lower() or "pendiente" in body["message"].lower()

    for event in body["events"]:
        assert "SERNAGEOMIN" in event["source"]
        assert event["location_certainty"] in ("verified", "approximate", "unverified_candidate")
        assert event["verification_status"] in ("verified", "pending_review")
        assert event["hazard_type"] in ("aluvion", "remocion_en_masa", "inundacion")
        assert event["date"]
        assert event["approx_location"]["lat"] is not None
        assert event["approx_location"]["lon"] is not None


def test_only_hand_curated_events_are_marked_verified(client):
    """El lote importado masivamente (catálogo de terceros, licencia pendiente)
    NUNCA debe marcarse 'verified': solo eventos investigados uno a uno a mano
    pueden llevar ese estado (ver docs/DECISIONES.md)."""
    response = client.get("/v1/events")
    body = response.json()
    verified_ids = {e["id"] for e in body["events"] if e["verification_status"] == "verified"}
    assert verified_ids == _ALLOWED_VERIFIED_IDS


def test_bulk_imported_batch_discloses_pending_license_in_source(client):
    """Cada evento del lote importado debe decir explícitamente que la fuente
    no es un canal oficial y que la licencia está pendiente, no solo citar
    SERNAGEOMIN sin matices."""
    response = client.get("/v1/events")
    body = response.json()
    pending = [e for e in body["events"] if e["verification_status"] == "pending_review"]
    assert len(pending) >= 50  # el lote real tiene ~113; cota amplia para no ser frágil
    for event in pending:
        assert "no es un canal oficial de SERNAGEOMIN" in event["source"]


def test_events_message_does_not_claim_pending_review_events_are_verified(client, monkeypatch):
    """Hallazgo de revisión PR #2: el mensaje no debe describir TODO el listado
    como 'verificado' si incluye registros verification_status='pending_review'."""
    mixed_events = [
        EventRecord(
            id="test-verified",
            date="2020-01-01",
            approx_location={"lat": -33.6, "lon": -70.3, "place": "test", "radius_km": 5},
            hazard_type="aluvion",
            source="SERNAGEOMIN, test, https://example.org/test",
            location_certainty="approximate",
            verification_status="verified",
            notes="evento de prueba",
        ),
        EventRecord(
            id="test-pending",
            date="2021-01-01",
            approx_location={"lat": -33.6, "lon": -70.3, "place": "test", "radius_km": 5},
            hazard_type="remocion_en_masa",
            source="SERNAGEOMIN (vía catálogo de terceros, no es un canal oficial de SERNAGEOMIN), test",
            location_certainty="unverified_candidate",
            verification_status="pending_review",
            notes="evento de prueba pendiente",
        ),
    ]
    monkeypatch.setattr(events_data, "EVENTS", mixed_events)
    # El router importó `EVENTS` por valor en su módulo; parcheamos también ahí.
    import app.routers.events as events_router

    monkeypatch.setattr(events_router, "EVENTS", mixed_events)

    response = client.get("/v1/events")
    body = response.json()
    assert "1 evento(s) verificado(s)" in body["message"]
    assert "1 evento(s) pendiente(s) de revisión" in body["message"]


def test_events_does_not_include_unverified_las_condes_2026_candidate(client):
    """docs/ALUVIONES_Y_PREVENCION.md: el candidato de Las Condes 2026 NO debe incorporarse
    sin fuente oficial/localización verificada."""
    response = client.get("/v1/events")
    body = response.json()
    event_ids = [event["id"] for event in body["events"]]
    assert not any("las-condes" in event_id.lower() for event_id in event_ids)
    assert not any("2026" in event_id for event_id in event_ids)


def test_bulk_batch_does_not_duplicate_the_hand_curated_2017_report(client):
    """El informe RM-2017-23 ya está cubierto a mano (resumido); sus 17
    sub-eventos no deben aparecer también como entradas pending_review
    separadas (ver pipelines/sernageomin_unab_catalog/fetch_and_filter.py)."""
    response = client.get("/v1/events")
    body = response.json()
    event_ids = [event["id"] for event in body["events"]]
    assert not any("RM-2017-23" in event_id for event_id in event_ids)
