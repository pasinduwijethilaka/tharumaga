from datetime import date

from backend.app.dasha_interpretation_engine import (
    TharuMagaDashaInterpretationEngine,
)


def make_chart():
    return {
        "planets": {
            "Sun": {
                "sign": "Sagittarius",
                "house": 3,
                "nakshatra": {
                    "name": "Purva Ashadha",
                    "lord": "Venus",
                    "pada": 4,
                },
            },
            "Moon": {
                "sign": "Capricorn",
                "house": 4,
                "nakshatra": {
                    "name": "Dhanishta",
                    "lord": "Mars",
                    "pada": 2,
                },
            },
            "Mars": {
                "sign": "Aquarius",
                "house": 5,
                "nakshatra": {
                    "name": "Shatabhisha",
                    "lord": "Rahu",
                    "pada": 2,
                },
            },
            "Mercury": {
                "sign": "Sagittarius",
                "house": 3,
                "nakshatra": {
                    "name": "Purva Ashadha",
                    "lord": "Venus",
                    "pada": 3,
                },
            },
            "Jupiter": {
                "sign": "Aries",
                "house": 7,
                "nakshatra": {
                    "name": "Ashwini",
                    "lord": "Ketu",
                    "pada": 1,
                },
            },
            "Venus": {
                "sign": "Scorpio",
                "house": 2,
                "nakshatra": {
                    "name": "Jyeshtha",
                    "lord": "Mercury",
                    "pada": 1,
                },
            },
            "Saturn": {
                "sign": "Aries",
                "house": 7,
                "nakshatra": {
                    "name": "Bharani",
                    "lord": "Venus",
                    "pada": 1,
                },
                "retrograde": True,
            },
            "Rahu": {
                "sign": "Cancer",
                "house": 10,
                "retrograde": True,
            },
            "Ketu": {
                "sign": "Capricorn",
                "house": 4,
                "retrograde": True,
            },
        },
        "dasha": [
            {
                "lord": "Jupiter",
                "start": "2021-12-16",
                "end": "2037-12-16",
                "years": 16,
                "antardasha": [
                    {
                        "lord": "Jupiter",
                        "start": "2021-12-16",
                        "end": "2024-01-12",
                        "years": 2.08,
                        "pratyantardasha": [],
                    },
                    {
                        "lord": "Mercury",
                        "start": "2026-08-16",
                        "end": "2028-11-21",
                        "years": 2.27,
                        "pratyantardasha": [
                            {
                                "lord": "Mercury",
                                "start": "2026-08-16",
                                "end": "2026-12-12",
                            }
                        ],
                    },
                ],
            }
        ],
        "rahu": {
            "sign": "Cancer",
            "house": 10,
        },
        "ketu": {
            "sign": "Capricorn",
            "house": 4,
        },
    }


def check(name, condition):
    if condition:
        print(f"PASS : {name}")
        return True

    print(f"FAIL : {name}")
    return False


def test_result_contract():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    result = engine.generate()

    return (
        result.get("available") is True
        and "as_of" in result
        and "current" in result
        and "periods" in result
        and "combined_text" in result
    )


def test_mahadasha_interpretation():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    result = engine.generate()
    maha = result["current"]["mahadasha"]

    return (
        maha["planet"] == "Jupiter"
        and maha["planet_si"] == "ගුරු"
        and maha["level"] == "Mahadasha"
        and maha["level_si"] == "මහ දශාව"
        and maha["available"] is True
        and maha["house"] == 7
        and "ගුරු" in maha["text"]
    )


def test_antardasha_interpretation():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    result = engine.generate()
    antar = result["current"]["antardasha"]

    return (
        antar is not None
        and antar["planet"] == "Mercury"
        and antar["planet_si"] == "බුධ"
        and antar["level"] == "Antardasha"
        and antar["level_si"] == "අන්තර් දශාව"
        and antar["available"] is True
    )


def test_pratyantardasha_interpretation():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    result = engine.generate()
    praty = result["current"]["pratyantardasha"]

    return (
        praty is not None
        and praty["planet"] == "Mercury"
        and praty["planet_si"] == "බුධ"
        and praty["level"] == "Pratyantardasha"
        and praty["level_si"] == "ප්‍රත්‍යන්තර දශාව"
        and praty["available"] is True
    )


def test_all_9_dasha_lords():
    engine = TharuMagaDashaInterpretationEngine(make_chart())

    expected = {
        "Sun": "රවි",
        "Moon": "සඳු",
        "Mars": "කුජ",
        "Mercury": "බුධ",
        "Jupiter": "ගුරු",
        "Venus": "සිකුරු",
        "Saturn": "ශනි",
        "Rahu": "රාහු",
        "Ketu": "කේතු",
    }

    return all(
        engine.planet_si(planet) == sinhala
        for planet, sinhala in expected.items()
    )


def test_planet_context():
    engine = TharuMagaDashaInterpretationEngine(make_chart())

    context = engine.build_planet_context("Jupiter")

    return (
        context["available"] is True
        and context["planet"] == "Jupiter"
        and context["planet_si"] == "ගුරු"
        and context["sign"] == "Aries"
        and context["sign_si"] == "මේෂ"
        and context["house"] == 7
        and context["nakshatra"] == "Ashwini"
        and context["nakshatra_lord"] == "Ketu"
        and context["pada"] == 1
    )


def test_house_and_sign_lord_context():
    engine = TharuMagaDashaInterpretationEngine(make_chart())

    context = engine.build_planet_context("Jupiter")

    return (
        context["sign_lord"] == "Mars"
        and context["sign_lord_si"] == "කුජ"
        and context["sign_lord_house"] == 5
    )


def test_nakshatra_context():
    engine = TharuMagaDashaInterpretationEngine(make_chart())

    context = engine.build_planet_context("Moon")

    return (
        context["nakshatra"] == "Dhanishta"
        and context["nakshatra_lord"] == "Mars"
        and context["nakshatra_lord_si"] == "කුජ"
        and context["pada"] == 2
    )


def test_missing_planet_is_safe():
    chart = make_chart()
    chart["planets"].pop("Jupiter")

    engine = TharuMagaDashaInterpretationEngine(
        chart,
        as_of=date(2026, 9, 1),
    )

    result = engine.interpret_planet_period(
        "Jupiter",
        "Mahadasha",
    )

    return (
        result["available"] is False
        and result["planet"] == "Jupiter"
        and result["planet_si"] == "ගුරු"
        and result["level"] == "Mahadasha"
        and result["level_si"] == "මහ දශාව"
        and "දත්ත ලබාගෙන නොමැත" in result["text"]
    )


def test_invalid_planets_container_is_safe():
    chart = make_chart()
    chart["planets"] = None

    engine = TharuMagaDashaInterpretationEngine(
        chart,
        as_of=date(2026, 9, 1),
    )

    result = engine.interpret_planet_period(
        "Jupiter",
        "Mahadasha",
    )

    return (
        result["available"] is False
        and result["planet_si"] == "ගුරු"
    )


def test_invalid_dasha_container_is_safe():
    chart = make_chart()

    malformed_cases = [
        None,
        "invalid",
        {},
        [None, "bad", 123],
    ]

    for malformed in malformed_cases:
        test_chart = make_chart()
        test_chart["dasha"] = malformed

        engine = TharuMagaDashaInterpretationEngine(
            test_chart,
            as_of=date(2026, 9, 1),
        )

        result = engine.find_current_period()

        if result != {
            "mahadasha": None,
            "antardasha": None,
            "pratyantardasha": None,
        }:
            return False

    return True


def test_date_handling_and_period_boundaries():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    return (
        engine.is_in_period(
            date(2026, 8, 16),
            "2026-08-16",
            "2028-11-21",
        )
        and engine.is_in_period(
            date(2026, 11, 20),
            "2026-08-16",
            "2028-11-21",
        )
        and not engine.is_in_period(
            date(2028, 11, 21),
            "2026-08-16",
            "2028-11-21",
        )
    )


def test_no_current_period_is_safe():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2050, 1, 1),
    )

    result = engine.generate()

    return (
        result["available"] is False
        and result["current"] == {}
        and "message" in result
    )


def test_combined_text():
    engine = TharuMagaDashaInterpretationEngine(
        make_chart(),
        as_of=date(2026, 9, 1),
    )

    result = engine.generate()
    text = result["combined_text"]

    return (
        "ගුරු" in text
        and "බුධ" in text
        and "මහ දශාව" in text
        and "අන්තර් දශාව" in text
        and "ප්‍රත්‍යන්තර දශාව" in text
    )


def test_retrograde_context():
    engine = TharuMagaDashaInterpretationEngine(make_chart())

    result = engine.interpret_planet_period(
        "Saturn",
        "Mahadasha",
    )

    return (
        result["retrograde"] is True
        and "වක්‍ර ගමනක" in result["text"]
    )


def main():
    print()
    print("THARUMAGA DASHA INTERPRETATION DEEP AUDIT")
    print()

    tests = [
        ("test_result_contract", test_result_contract),
        ("test_mahadasha_interpretation", test_mahadasha_interpretation),
        ("test_antardasha_interpretation", test_antardasha_interpretation),
        ("test_pratyantardasha_interpretation", test_pratyantardasha_interpretation),
        ("test_all_9_dasha_lords", test_all_9_dasha_lords),
        ("test_planet_context", test_planet_context),
        ("test_house_and_sign_lord_context", test_house_and_sign_lord_context),
        ("test_nakshatra_context", test_nakshatra_context),
        ("test_missing_planet_is_safe", test_missing_planet_is_safe),
        ("test_invalid_planets_container_is_safe", test_invalid_planets_container_is_safe),
        ("test_invalid_dasha_container_is_safe", test_invalid_dasha_container_is_safe),
        ("test_date_handling_and_period_boundaries", test_date_handling_and_period_boundaries),
        ("test_no_current_period_is_safe", test_no_current_period_is_safe),
        ("test_combined_text", test_combined_text),
        ("test_retrograde_context", test_retrograde_context),
    ]

    passed = 0

    for name, test in tests:
        try:
            if check(name, test()):
                passed += 1
        except Exception as error:
            print(f"FAIL : {name}")
            print(f"       ERROR: {error}")

    print()
    print(f"RESULT: {passed}/{len(tests)} audit tests passed")


if __name__ == "__main__":
    main()