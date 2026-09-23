"""
TharuMaga Yoga Detection Engine v1.2 regression tests.

Run from project root:
    python -m backend.app.test_yoga_detection_v1_2
"""

from .astrology_engine import TharuMagaEngine
from .yoga_detection_engine import TharuMagaYogaEngine


def build_reference_chart():
    return TharuMagaEngine(
        day=10,
        month=1,
        year=2000,
        hour=2,
        minute=25,
        second=0,
        latitude=6.9271,
        longitude=79.8612,
        timezone="Asia/Colombo",
        place="Colombo, Sri Lanka",
    ).calculate()


def synthetic_chart(lagna: str, planets: dict) -> dict:
    return {
        "lagna": {"sign": lagna},
        "planets": planets,
    }


def p(sign: str, house: int) -> dict:
    return {"sign": sign, "house": house}


def get_yoga(result, yoga_id):
    for yoga in result["yogas"]:
        if yoga["id"] == yoga_id:
            return yoga
    raise AssertionError(f"Yoga not found: {yoga_id}")


def test_reference_contract():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    assert result["version"] == "1.2"
    assert result["relationship_model"]["mutual_aspect"] is True
    assert result["relationship_model"]["sign_exchange"] is True


def test_reference_core_yogas():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    ids = {y["id"] for y in result["yogas"]}

    assert {"gaja_kesari", "budha_aditya", "raja_yoga", "dhana_yoga"} <= ids


def test_reference_raja_has_same_lord():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    yoga = get_yoga(result, "raja_yoga")

    assert "same_lord" in yoga["relationships"]
    assert "Saturn" in yoga["planets"]


def test_reference_dhana_keeps_sun_mercury():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    yoga = get_yoga(result, "dhana_yoga")

    assert {"Mercury", "Sun"} <= set(yoga["planets"])


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


def test_dharma_karmadhipati_mutual_aspect():
    chart = synthetic_chart(
        "Aries",
        {
            "Jupiter": p("Cancer", 4),
            "Saturn": p("Capricorn", 10),
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_dharma_karmadhipati()

    assert yoga is not None
    assert "mutual_aspect" in yoga["relationships"]


def test_dharma_karmadhipati_sign_exchange():
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


def test_raja_yoga_mutual_aspect():
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


def test_dhana_yoga_mutual_aspect():
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


def test_no_false_raja_without_lord_relationship():
    # Gemini Lagna:
    # 5th lord Venus and 9th lord Saturn have no qualifying relationship
    # with the Kendra lords Mercury/Jupiter in this synthetic chart.
    chart = synthetic_chart(
        "Gemini",
        {
            "Mercury": p("Gemini", 1),      # 1st/4th lord
            "Venus": p("Cancer", 2),        # 5th lord
            "Saturn": p("Leo", 3),           # 9th lord
            "Jupiter": p("Scorpio", 6),      # 7th/10th lord
        },
    )
    yoga = TharuMagaYogaEngine(chart).detect_raja_yoga()

    assert yoga is None


def test_pancha_mahapurusha_reference_absent():
    result = TharuMagaYogaEngine(build_reference_chart()).generate()
    assert not any(
        yoga["id"].startswith("mahapurusha_")
        for yoga in result["yogas"]
    )


def run():
    tests = [
        test_reference_contract,
        test_reference_core_yogas,
        test_reference_raja_has_same_lord,
        test_reference_dhana_keeps_sun_mercury,
        test_mutual_aspect_helper,
        test_sign_exchange_helper,
        test_dharma_karmadhipati_mutual_aspect,
        test_dharma_karmadhipati_sign_exchange,
        test_raja_yoga_mutual_aspect,
        test_dhana_yoga_mutual_aspect,
        test_no_false_raja_without_lord_relationship,
        test_pancha_mahapurusha_reference_absent,
    ]

    passed = 0

    print("=" * 68)
    print("THARUMAGA YOGA DETECTION v1.2 REGRESSION TEST")
    print("=" * 68)

    for test_fn in tests:
        try:
            test_fn()
            print("PASS", test_fn.__name__)
            passed += 1
        except AssertionError as error:
            print("FAIL", test_fn.__name__, "-", error)

    print("-" * 68)
    print(f"RESULT: {passed}/{len(tests)} regression tests passed")
    print("=" * 68)

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run()
