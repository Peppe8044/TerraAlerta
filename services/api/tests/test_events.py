from __future__ import annotations


def test_events_endpoint_returns_empty_list_with_explicit_message(client):
    """Gate: no simular aluviones reales (docs/AUDITORIA_MVP_2026-10-14.md)."""
    response = client.get("/v1/events")
    assert response.status_code == 200
    body = response.json()
    assert body["events"] == []
    assert "verificad" in body["message"].lower()
