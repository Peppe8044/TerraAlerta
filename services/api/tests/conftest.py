from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


# Coordenada dentro del bounding box piloto de San José de Maipo (ver app/config.py).
SAN_JOSE_DE_MAIPO = {"lat": -33.6378, "lon": -70.3539}
# Coordenada claramente fuera de cobertura (Punta Arenas).
OUT_OF_COVERAGE = {"lat": -53.1638, "lon": -70.9171}
