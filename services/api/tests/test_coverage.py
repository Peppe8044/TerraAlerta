from __future__ import annotations

from app.coverage import check_coverage


def test_point_inside_san_jose_de_maipo_bbox_is_in_coverage():
    result = check_coverage(-33.6378, -70.3539)
    assert result.in_coverage is True
    assert result.reason is None


def test_point_far_outside_pilot_zone_is_rejected():
    result = check_coverage(-53.1638, -70.9171)
    assert result.in_coverage is False
    assert "zona piloto" in result.reason


def test_invalid_coordinates_are_rejected():
    result = check_coverage(999.0, 999.0)
    assert result.in_coverage is False
