"""
TharuMaga Yoga Detection Regression Tests

Run from project root:
    python -m backend.app.test_yoga_detection
"""

from backend.app.astrology_engine import TharuMagaEngine
from backend.app.yoga_detection_engine import TharuMagaYogaEngine


CHART_2000 = {
    "day": 10, "month": 1, "year": 2000,
    "hour": 2, "minute": 25, "second": 0,
    "latitude": 6.9271, "longitude": 79.8612,
    "timezone": "Asia/Colombo",
    "place": "Colombo, Sri Lanka",
}


def chart():
    return TharuMagaEngine(**CHART_2000).calculate()


def yogas():
    return TharuMagaYogaEngine(chart()).generate()["yogas"]


def yoga_ids():
    return {item["id"] for item in yogas()}


def get_yoga(yoga_id):
    for item in yogas():
        if item["id"] == yoga_id:
            return item
    raise AssertionError(f"Yoga not found: {yoga_id}")


def test_engine_contract():
    result = TharuMagaYogaEngine(chart()).generate()

    assert result["engine"] == "TharuMaga Yoga Detection Engine"
    assert result["version"] == "1.0"
    assert result["system"] == "Traditional Vedic/Jyotisha rule detection"
    assert result["house_system"] == "Whole Sign"
    assert result["count"] == len(result["yogas"])


def test_expected_yogas_detected():
    assert yoga_ids() == {
        "gaja_kesari",
        "budha_aditya",
        "raja_yoga",
        "dhana_yoga",
    }


def test_gaja_kesari():
    yoga = get_yoga("gaja_kesari")

    assert yoga["name"] == "Gaja Kesari Yoga"
    assert yoga["planets"] == ["Moon", "Jupiter"]
    assert yoga["houses"] == [4, 7]
    assert yoga["status"] == "detected"


def test_budha_aditya():
    yoga = get_yoga("budha_aditya")

    assert yoga["name"] == "Budha Aditya Yoga"
    assert yoga["planets"] == ["Sun", "Mercury"]
    assert yoga["houses"] == [3]
    assert yoga["status"] == "detected"


def test_raja_yoga():
    yoga = get_yoga("raja_yoga")

    assert yoga["name"] == "Raja Yoga"
    assert yoga["planets"] == ["Saturn"]
    assert yoga["houses"] == [4, 5]
    assert yoga["status"] == "detected"


def test_dhana_yoga():
    yoga = get_yoga("dhana_yoga")

    assert yoga["name"] == "Dhana Yoga"
    assert yoga["planets"] == ["Mercury", "Sun"]
    assert yoga["houses"] == [9, 11]
    assert yoga["status"] == "detected"


def test_no_pancha_mahapurusha_for_reference_chart():
    result = TharuMagaYogaEngine(chart()).generate()

    assert not any(
        item["category"] == "Pancha Mahapurusha"
        for item in result["yogas"]
    )


def test_yoga_result_contract():
    for yoga in yogas():
        for key in (
            "id",
            "name",
            "category",
            "status",
            "planets",
            "houses",
            "rule",
        ):
            assert key in yoga

        assert yoga["status"] == "detected"
        assert isinstance(yoga["planets"], list)
        assert isinstance(yoga["houses"], list)
        assert yoga["rule"]


def run_all():
    tests = [
        test_engine_contract,
        test_expected_yogas_detected,
        test_gaja_kesari,
        test_budha_aditya,
        test_raja_yoga,
        test_dhana_yoga,
        test_no_pancha_mahapurusha_for_reference_chart,
        test_yoga_result_contract,
    ]

    print("=" * 68)
    print("THARUMAGA YOGA DETECTION REGRESSION TEST")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS  {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} regression tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()
