"""
TharuMaga Dhana Yoga False-Positive Audit

Run from project root:

    python -m backend.app.test_dhana_yoga_false_positive

Purpose:
- Check that Dhana Yoga is NOT detected when the
  2nd, 5th, 9th and 11th lords have no qualifying
  relationship.

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


def test_no_dhana_without_wealth_lord_relationship():
    """
    Aries Lagna:

        2nd house  Taurus      -> Venus
        5th house  Leo         -> Sun
        9th house  Sagittarius -> Jupiter
        11th house Aquarius    -> Saturn

    Placements:

        Venus   -> 1st house
        Sun     -> 2nd house
        Jupiter -> 3rd house
        Saturn  -> 4th house

    The four wealth-house lords are intentionally placed
    without conjunction, mutual aspect or sign exchange.

    Therefore the current structural Dhana rule should
    return None.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Venus": p("Aries", 1),
            "Sun": p("Taurus", 2),
            "Jupiter": p("Gemini", 3),
            "Saturn": p("Cancer", 4),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is None, (
        "False positive: Dhana Yoga detected even though "
        "the wealth-house lords have no qualifying relationship."
    )

    print("PASS : no Dhana Yoga without qualifying relationship")


def test_no_dhana_with_unrelated_planets():
    """
    Control case:

    Only non-wealth planets are supplied.

    The engine should not invent a Dhana Yoga when the
    relevant wealth-house lords are unavailable.
    """

    chart = synthetic_chart(
        "Aries",
        {
            "Mars": p("Cancer", 4),
            "Moon": p("Leo", 5),
        },
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is None, (
        "False positive: Dhana Yoga detected without "
        "the required wealth-house lords."
    )

    print("PASS : no Dhana Yoga with unrelated planets only")


def test_no_dhana_with_empty_chart():
    """
    Empty chart control.

    No planetary information exists, so Dhana Yoga
    must not be detected.
    """

    chart = synthetic_chart(
        "Aries",
        {},
    )

    yoga = TharuMagaYogaEngine(chart).detect_dhana_yoga()

    assert yoga is None, (
        "False positive: Dhana Yoga detected from an empty chart."
    )

    print("PASS : no Dhana Yoga from empty chart")


def run():
    tests = [
        test_no_dhana_without_wealth_lord_relationship,
        test_no_dhana_with_unrelated_planets,
        test_no_dhana_with_empty_chart,
    ]

    passed = 0

    print("=" * 68)
    print("THARUMAGA DHANA YOGA FALSE-POSITIVE AUDIT")
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