from __future__ import annotations

ALLOWED_LICENSE_STATUSES = {"approved", "pending", "research_only", "blocked"}


def test_sources_lists_all_registered_datasets(client):
    response = client.get("/v1/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) > 0


def test_sources_have_required_governance_fields(client):
    response = client.get("/v1/sources")
    sources = response.json()
    for source in sources:
        assert source["license_status"] in ALLOWED_LICENSE_STATUSES
        assert source["url"].startswith("http")
        assert source["last_verified"]
        assert source["notes"]


def test_no_paid_or_unapproved_source_is_silently_treated_as_approved(client):
    """Gate G0: una URL pública no prueba licencia; solo Open-Meteo está 'approved'."""
    response = client.get("/v1/sources")
    sources = {s["dataset"]: s for s in response.json()}
    approved = [d for d, s in sources.items() if s["license_status"] == "approved"]
    assert all("Open-Meteo" in d for d in approved)
