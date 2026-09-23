"""
TharuMaga Pancha Mahapurusha Yoga Deep Audit

Run from project root:

    python -m backend.app.test_pancha_mahapurusha_audit

Purpose:
- Test each of the five Pancha Mahapurusha Yogas.
- Test Kendra requirement.
- Test own/exaltation sign requirement.
- Test false-positive protection.

Current structural rule:
    Planet must be in a Kendra (1, 4, 7, 10)
    AND
    Planet must be in its own or exaltation sign.

This test does NOT modify the Yoga Detection Engine.
"""

from .yoga_detection_engine import TharuMagaYogaEngine


def synthetic_chart(lagna: str, planets: dict) -> dict:
    return {
        "lagna": {"sign": lagna},
        "planets": planets,
    }


def p(sign: str, house: int) -> dict:
    return {
        "sign": sign,
        "house": house,
    }


def get_mahapurusha(yogas: list[dict], planet: str):
    yoga_id = f"mahapurusha_{planet.lower()}"

    for yoga in yogas:
        if yoga["id"] == yoga_id:
            return yoga

    return None


# ================================================================
# POSITIVE TESTS
# ================================================================

def test_ruchaka_mars():
    """
    Mars:
        Own signs       = Aries / Scorpio
        Exaltation      = Capricorn
        Kendra required

    Mars in Aries, 1st house -> Ruchaka Yoga.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Mars": p("Aries", 1),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Mars")

    assert yoga is not None
    assert yoga["name"] == "Ruchaka Yoga"
    assert yoga["category"] == "Pancha Mahapurusha"
    assert yoga["houses"] == [1]

    print("PASS : Mars -> Ruchaka Yoga")


def test_bhadra_mercury():
    """
    Mercury:
        Own signs       = Gemini / Virgo
        Exaltation      = Virgo
        Kendra required

    Mercury in Gemini, 1st house -> Bhadra Yoga.
    """

    chart = synthetic_chart(
        "Gemini",
        {
            "Mercury": p("Gemini", 1),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Mercury")

    assert yoga is not None
    assert yoga["name"] == "Bhadra Yoga"
    assert yoga["category"] == "Pancha Mahapurusha"
    assert yoga["houses"] == [1]

    print("PASS : Mercury -> Bhadra Yoga")


def test_hamsa_jupiter():
    """
    Jupiter:
        Own signs       = Sagittarius / Pisces
        Exaltation      = Cancer
        Kendra required

    Jupiter in Cancer, 10th house -> Hamsa Yoga.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Jupiter": p("Cancer", 10),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Jupiter")

    assert yoga is not None
    assert yoga["name"] == "Hamsa Yoga"
    assert yoga["category"] == "Pancha Mahapurusha"
    assert yoga["houses"] == [10]

    print("PASS : Jupiter -> Hamsa Yoga")


def test_malavya_venus():
    """
    Venus:
        Own signs       = Taurus / Libra
        Exaltation      = Pisces
        Kendra required

    Venus in Libra, 1st house -> Malavya Yoga.
    """

    chart = synthetic_chart(
        "Libra",
        {
            "Venus": p("Libra", 1),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Venus")

    assert yoga is not None
    assert yoga["name"] == "Malavya Yoga"
    assert yoga["category"] == "Pancha Mahapurusha"
    assert yoga["houses"] == [1]

    print("PASS : Venus -> Malavya Yoga")


def test_sasa_saturn():
    """
    Saturn:
        Own signs       = Capricorn / Aquarius
        Exaltation      = Libra
        Kendra required

    Saturn in Aquarius, 1st house -> Sasa Yoga.
    """

    chart = synthetic_chart(
        "Aquarius",
        {
            "Saturn": p("Aquarius", 1),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Saturn")

    assert yoga is not None
    assert yoga["name"] == "Sasa Yoga"
    assert yoga["category"] == "Pancha Mahapurusha"
    assert yoga["houses"] == [1]

    print("PASS : Saturn -> Sasa Yoga")


# ================================================================
# KENDRA TESTS
# ================================================================

def test_kendra_house_4_is_valid():
    """
    Planet in 4th house is a Kendra.

    Mars in Scorpio, 4th house -> Ruchaka Yoga.
    """

    chart = synthetic_chart(
        "Leo",
        {
            "Mars": p("Scorpio", 4),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Mars")

    assert yoga is not None
    assert yoga["houses"] == [4]

    print("PASS : Kendra house 4 accepted")


def test_kendra_house_7_is_valid():
    """
    Planet in 7th house is a Kendra.

    Venus in Pisces, 7th house -> Malavya Yoga.
    """

    chart = synthetic_chart(
        "Virgo",
        {
            "Venus": p("Pisces", 7),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Venus")

    assert yoga is not None
    assert yoga["houses"] == [7]

    print("PASS : Kendra house 7 accepted")


# ================================================================
# NEGATIVE TESTS
# ================================================================

def test_non_kendra_house_rejected():
    """
    Mars is in its own sign Aries,
    but the planet is in the 2nd house.

    2nd house is NOT a Kendra.

    Therefore Ruchaka Yoga must NOT be detected.
    """

    chart = synthetic_chart(
        "Pisces",
        {
            "Mars": p("Aries", 2),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Mars")

    assert yoga is None

    print("PASS : Non-Kendra house rejected")


def test_wrong_sign_in_kendra_rejected():
    """
    Mars is in the 1st house (Kendra),
    but Mars is in Gemini, which is not
    an own/exaltation sign for Mars.

    Therefore Ruchaka Yoga must NOT be detected.
    """

    chart = synthetic_chart(
        "Gemini",
        {
            "Mars": p("Gemini", 1),
        },
    )

    result = TharuMagaYogaEngine(chart).generate()
    yoga = get_mahapurusha(result["yogas"], "Mars")

    assert yoga is None

    print("PASS : Wrong sign in Kendra rejected")


def test_empty_chart_has_no_mahapurusha():
    """
    No planetary data.

    No Pancha Mahapurusha Yoga should be detected.
    """

    chart = synthetic_chart(
        "Aries",
        {},
    )

    result = TharuMagaYogaEngine(chart).generate()

    mahapurusha = [
        yoga
        for yoga in result["yogas"]
        if yoga["category"] == "Pancha Mahapurusha"
    ]

    assert mahapurusha == []

    print("PASS : Empty chart has no Mahapurusha Yoga")


# ================================================================
# RUNNER
# ================================================================

def run():
    tests = [
        test_ruchaka_mars,
        test_bhadra_mercury,
        test_hamsa_jupiter,
        test_malavya_venus,
        test_sasa_saturn,
        test_kendra_house_4_is_valid,
        test_kendra_house_7_is_valid,
        test_non_kendra_house_rejected,
        test_wrong_sign_in_kendra_rejected,
        test_empty_chart_has_no_mahapurusha,
    ]

    passed = 0

    print("=" * 68)
    print("THARUMAGA PANCHA MAHAPURUSHA YOGA DEEP AUDIT")
    print("=" * 68)

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as error:
            print("FAIL", test_fn.__name__, "-", error)

    print("-" * 68)
    print(f"RESULT: {passed}/{len(tests)} audit tests passed")
    print("=" * 68)

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run()