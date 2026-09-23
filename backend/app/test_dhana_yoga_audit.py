"""
TharuMaga Dhana Yoga Deep Audit Tests

Run from project root:

    python -m backend.app.test_dhana_yoga_audit

Purpose:
- Audit each wealth-house pair independently.
- Do NOT modify the Yoga Detection Engine.
- Test the current v1.2 relationship model.

Wealth houses:
    2, 5, 9, 11

Pairs:
    2-5
    2-9
    2-11
    5-9
    5-11
    9-11
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


def test_2_5_same_lord():
    """
    Aries Lagna:
        2nd house  = Taurus  -> Venus
        5th house  = Leo     -> Sun

    This test uses the 2nd and 5th lords in the same house.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Venus": p("Gemini", 3),
            "Sun": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 2 ↔ 5 : conjunction")


def test_2_9_same_lord():
    """
    Aries Lagna:
        2nd house = Taurus      -> Venus
        9th house = Sagittarius -> Jupiter

    Venus and Jupiter are placed together.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Venus": p("Gemini", 3),
            "Jupiter": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 2 ↔ 9 : conjunction")


def test_2_11_conjunction():
    """
    Aries Lagna:
        2nd house  = Taurus -> Venus
        11th house = Aquarius -> Saturn

    Venus and Saturn are placed together.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Venus": p("Gemini", 3),
            "Saturn": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 2 ↔ 11 : conjunction")


def test_5_9_conjunction():
    """
    Aries Lagna:
        5th house = Leo        -> Sun
        9th house = Sagittarius -> Jupiter

    Sun and Jupiter are placed together.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Sun": p("Gemini", 3),
            "Jupiter": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 5 ↔ 9 : conjunction")


def test_5_11_conjunction():
    """
    Aries Lagna:
        5th house  = Leo      -> Sun
        11th house = Aquarius -> Saturn

    Sun and Saturn are placed together.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Sun": p("Gemini", 3),
            "Saturn": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 5 ↔ 11 : conjunction")


def test_9_11_conjunction():
    """
    Aries Lagna:
        9th house  = Sagittarius -> Jupiter
        11th house = Aquarius    -> Saturn

    Jupiter and Saturn are placed together.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Jupiter": p("Gemini", 3),
            "Saturn": p("Gemini", 3),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is not None
    assert "conjunction" in yoga["relationships"]

    print("PASS 9 ↔ 11 : conjunction")


def test_existing_mutual_aspect_case():
    """
    Existing v1.2 regression case.

    Aries Lagna:
        2nd house = Taurus -> Venus
        11th house = Aquarius -> Saturn

    Venus in Cancer (4th)
    Saturn in Capricorn (10th)

    This should continue to detect Dhana Yoga
    through mutual aspect.
    """

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

    print("PASS existing mutual aspect : 2 ↔ 11")


def run():
    tests = [
        test_2_5_same_lord,
        test_2_9_same_lord,
        test_2_11_conjunction,
        test_5_9_conjunction,
        test_5_11_conjunction,
        test_9_11_conjunction,
        test_existing_mutual_aspect_case,
    ]

    passed = 0

    print("=" * 68)
    print("THARUMAGA DHANA YOGA DEEP AUDIT")
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