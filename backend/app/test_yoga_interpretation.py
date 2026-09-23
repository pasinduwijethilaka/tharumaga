"""
TharuMaga Yoga Interpretation Engine regression tests
"""
from __future__ import annotations

from .astrology_engine import TharuMagaEngine
from .yoga_detection_engine import TharuMagaYogaEngine
from .yoga_interpretation_engine import TharuMagaYogaInterpretationEngine


def build_reference_chart():
    return TharuMagaEngine(
        day=10, month=1, year=2000, hour=2, minute=25, second=0,
        latitude=6.9271, longitude=79.8612,
        timezone="Asia/Colombo", place="Colombo, Sri Lanka",
    ).calculate()


def build_interpretation():
    chart = build_reference_chart()
    detected = TharuMagaYogaEngine(chart).generate()
    return TharuMagaYogaInterpretationEngine(detected).generate()


def test_engine_contract():
    result = build_interpretation()
    assert result["engine"] == "TharuMaga Yoga Interpretation Engine"
    assert result["version"] == "1.0"
    assert isinstance(result["interpretations"], list)


def test_count_matches_cards():
    result = build_interpretation()
    assert result["count"] == len(result["interpretations"])


def test_reference_core_yogas_have_interpretations():
    result = build_interpretation()
    ids = {card["id"] for card in result["interpretations"]}
    assert {
        "gaja_kesari",
        "budha_aditya",
        "raja_yoga",
        "dhana_yoga",
    }.issubset(ids)


def test_gaja_kesari_profile():
    result = build_interpretation()
    card = next(x for x in result["interpretations"] if x["id"] == "gaja_kesari")
    assert card["title"] == "Gaja Kesari Yoga"
    assert "Moon" in card["planets"]
    assert "Jupiter" in card["planets"]
    assert len(card["themes"]) >= 3
    assert card["caution"]


def test_budha_aditya_profile():
    result = build_interpretation()
    card = next(x for x in result["interpretations"] if x["id"] == "budha_aditya")
    assert card["title"] == "Budha Aditya Yoga"
    assert set(card["planets"]) == {"Sun", "Mercury"}
    assert "communication" in card["themes"]


def test_raja_yoga_relationship_is_preserved():
    result = build_interpretation()
    card = next(x for x in result["interpretations"] if x["id"] == "raja_yoga")
    assert "same_lord" in card["relationships"]
    assert card["relationship_summary"]


def test_dhana_yoga_profile():
    result = build_interpretation()
    card = next(x for x in result["interpretations"] if x["id"] == "dhana_yoga")
    assert card["title"] == "Dhana Yoga"
    assert "resources" in card["themes"]
    assert card["caution"]


def test_unknown_yoga_is_safe():
    result = TharuMagaYogaInterpretationEngine({
        "engine": "TharuMaga Yoga Detection Engine",
        "version": "1.1",
        "yogas": [{
            "id": "future_test_yoga",
            "name": "Future Test Yoga",
            "category": "Test",
            "status": "detected",
            "planets": ["Sun"],
            "houses": [1],
            "rule": "Test rule",
        }],
    }).generate()

    assert result["count"] == 1
    assert result["interpretations"][0]["id"] == "future_test_yoga"
    assert result["interpretations"][0]["caution"]


def run():
    tests = [
        test_engine_contract,
        test_count_matches_cards,
        test_reference_core_yogas_have_interpretations,
        test_gaja_kesari_profile,
        test_budha_aditya_profile,
        test_raja_yoga_relationship_is_preserved,
        test_dhana_yoga_profile,
        test_unknown_yoga_is_safe,
    ]

    passed = 0
    print("=" * 68)
    print("THARUMAGA YOGA INTERPRETATION REGRESSION TEST")
    print("=" * 68)

    for test in tests:
        try:
            test()
            print("PASS ", test.__name__)
            passed += 1
        except AssertionError as error:
            print("FAIL ", test.__name__, "-", error)

    print("-" * 68)
    print(f"RESULT: {passed}/{len(tests)} regression tests passed")
    print("=" * 68)

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run()
