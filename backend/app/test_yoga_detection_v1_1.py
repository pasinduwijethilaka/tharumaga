"""
TharuMaga Yoga Detection Engine v1.1 regression tests
"""
from __future__ import annotations

from .astrology_engine import TharuMagaEngine
from .yoga_detection_engine import TharuMagaYogaEngine


def build_reference_chart():
    return TharuMagaEngine(
        day=10, month=1, year=2000, hour=2, minute=25, second=0,
        latitude=6.9271, longitude=79.8612,
        timezone="Asia/Colombo", place="Colombo, Sri Lanka",
    ).calculate()


def synthetic_chart(lagna: str, planets: dict) -> dict:
    return {
        "lagna": {"sign": lagna},
        "planets": planets,
    }


def p(sign: str, house: int) -> dict:
    return {"sign": sign, "house": house}


def test_reference_chart_contract():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    assert result["engine"] == "TharuMaga Yoga Detection Engine"
    assert result["version"] == "1.1"
    assert result["relationship_model"]["mutual_aspect"] is True
    assert result["relationship_model"]["sign_exchange"] is True


def test_reference_chart_keeps_core_yogas():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    ids = {y["id"] for y in result["yogas"]}
    expected = {
        "gaja_kesari",
        "budha_aditya",
        "raja_yoga",
        "dhana_yoga",
    }
    assert expected.issubset(ids)


def test_reference_raja_yoga_has_same_lord_relationship():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    yoga = next(y for y in result["yogas"] if y["id"] == "raja_yoga")
    assert "same_lord" in yoga["relationships"]
    assert "Saturn" in yoga["planets"]


def test_reference_dhana_yoga_has_wealth_family_relationship():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    yoga = next(y for y in result["yogas"] if y["id"] == "dhana_yoga")
    assert set(yoga["planets"]) >= {"Mercury", "Sun"}


def test_mutual_aspect_helper():
    chart = synthetic_chart(
        "Aries",
        {
            "Mars": p("Cancer", 4),
            "Jupiter": p("Capricorn", 10),
        },
    )
    engine = TharuMagaYogaEngine(chart)
    assert engine.mutual_aspect("Mars", "Jupiter") is True


def test_sign_exchange_helper():
    chart = synthetic_chart(
        "Aries",
        {
            "Mars": p("Libra", 7),
            "Venus": p("Aries", 1),
        },
    )
    engine = TharuMagaYogaEngine(chart)
    assert engine.sign_exchange("Mars", "Venus") is True


def test_dharma_karmadhipati_via_mutual_aspect():
    # Aries Lagna: 9th lord Jupiter, 10th lord Saturn.
    # Jupiter in Gemini (3), Saturn in Sagittarius (9): mutual 7th aspect.
    chart = synthetic_chart(
        "Aries",
        {
            "Jupiter": p("Gemini", 3),
            "Saturn": p("Sagittarius", 9),
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_dharma_karmadhipati()
    assert yoga is not None
    assert "mutual_aspect" in yoga["relationships"]


def test_dharma_karmadhipati_via_sign_exchange():
    # Aries Lagna: 9th lord Jupiter, 10th lord Saturn.
    # Jupiter in Capricorn (Saturn's sign), Saturn in Sagittarius (Jupiter's sign).
    chart = synthetic_chart(
        "Aries",
        {
            "Jupiter": p("Capricorn", 10),
            "Saturn": p("Sagittarius", 9),
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_dharma_karmadhipati()
    assert yoga is not None
    assert "sign_exchange" in yoga["relationships"]


def test_raja_yoga_via_mutual_aspect():
    # Aries Lagna: 5th lord Sun, 10th lord Saturn.
    # Sun in Cancer (4), Saturn in Capricorn (10): mutual 7th aspect.
    chart = synthetic_chart(
        "Aries",
        {
            "Sun": p("Cancer", 4),
            "Saturn": p("Capricorn", 10),
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_raja_yoga()
    assert yoga is not None
    assert "mutual_aspect" in yoga["relationships"]


def test_dhana_yoga_via_mutual_aspect():
    # Aries Lagna: 2nd lord Venus, 11th lord Saturn.
    # Venus in Cancer (4), Saturn in Capricorn (10): mutual 7th aspect.
    chart = synthetic_chart(
        "Aries",
        {
            "Venus": p("Cancer", 4),
            "Saturn": p("Capricorn", 10),
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()
    assert yoga is not None
    assert "mutual_aspect" in yoga["relationships"]


def test_pancha_mahapurusha_reference_remains_absent():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    ids = {y["id"] for y in result["yogas"]}
    assert not any(x.startswith("mahapurusha_") for x in ids)


def run():
    tests = [
        test_reference_chart_contract,
        test_reference_chart_keeps_core_yogas,
        test_reference_raja_yoga_has_same_lord_relationship,
        test_reference_dhana_yoga_has_wealth_family_relationship,
        test_mutual_aspect_helper,
        test_sign_exchange_helper,
        test_dharma_karmadhipati_via_mutual_aspect,
        test_dharma_karmadhipati_via_sign_exchange,
        test_raja_yoga_via_mutual_aspect,
        test_dhana_yoga_via_mutual_aspect,
        test_pancha_mahapurusha_reference_remains_absent,
    ]

    passed = 0
    print("=" * 68)
    print("THARUMAGA YOGA DETECTION v1.1 REGRESSION TEST")
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
