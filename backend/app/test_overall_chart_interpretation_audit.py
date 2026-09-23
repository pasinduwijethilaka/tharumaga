from backend.app.interpretation_engine import (
    TharuMagaInterpretationEngine,
)


def make_chart():
    return {
        "lagna": {
            "sign": "Libra",
            "nakshatra": {
                "name": "Vishakha",
                "lord": "Jupiter",
                "pada": 1,
            },
        },
        "planets": {
            "Sun": {
                "sign": "Sagittarius",
                "house": 3,
            },
            "Moon": {
                "sign": "Capricorn",
                "house": 4,
            },
            "Mars": {
                "sign": "Aquarius",
                "house": 5,
            },
            "Mercury": {
                "sign": "Sagittarius",
                "house": 3,
            },
            "Jupiter": {
                "sign": "Aries",
                "house": 7,
            },
            "Venus": {
                "sign": "Scorpio",
                "house": 2,
            },
            "Saturn": {
                "sign": "Aries",
                "house": 7,
                "retrograde": True,
            },
        },
        "rahu": {
            "sign": "Cancer",
            "house": 10,
            "retrograde": True,
        },
        "ketu": {
            "sign": "Capricorn",
            "house": 4,
            "retrograde": True,
        },
    }


def check(name, condition):
    if condition:
        print(f"PASS : {name}")
        return True

    print(f"FAIL : {name}")
    return False


def test_result_contract():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    return (
        isinstance(result, dict)
        and "lagna" in result
        and "moon" in result
        and "planets" in result
    )


def test_lagna_interpretation():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    lagna = result["lagna"]

    return (
        lagna["title"] == "ලග්න විශ්ලේෂණය"
        and lagna["sign"] == "තුලා"
        and lagna["nakshatra"] == "Vishakha"
        and "තුලා" in lagna["text"]
    )


def test_moon_interpretation():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    moon = result["moon"]

    return (
        moon["title"] == "සඳු සහ මානසික ස්වභාවය"
        and moon["sign"] == "මකර"
        and moon["house"] == 4
        and "මකර" in moon["text"]
        and "4" in moon["text"]
    )


def test_all_main_planets_present():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = result["planets"]

    names = {
        item["planet"]
        for item in planets
    }

    expected = {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "Rahu",
        "Ketu",
    }

    return expected.issubset(names)


def test_sinhala_planet_names():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

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
        planets[planet]["planet_si"] == sinhala
        for planet, sinhala in expected.items()
    )


def test_planet_sign_mapping():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

    return (
        planets["Sun"]["sign"] == "ධනු"
        and planets["Moon"]["sign"] == "මකර"
        and planets["Mars"]["sign"] == "කුම්භ"
        and planets["Mercury"]["sign"] == "ධනු"
        and planets["Jupiter"]["sign"] == "මේෂ"
        and planets["Venus"]["sign"] == "වෘශ්චික"
        and planets["Saturn"]["sign"] == "මේෂ"
        and planets["Rahu"]["sign"] == "කටක"
        and planets["Ketu"]["sign"] == "මකර"
    )


def test_planet_house_mapping():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

    return (
        planets["Sun"]["house"] == 3
        and planets["Moon"]["house"] == 4
        and planets["Mars"]["house"] == 5
        and planets["Mercury"]["house"] == 3
        and planets["Jupiter"]["house"] == 7
        and planets["Venus"]["house"] == 2
        and planets["Saturn"]["house"] == 7
        and planets["Rahu"]["house"] == 10
        and planets["Ketu"]["house"] == 4
    )


def test_retrograde_context():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

    return (
        planets["Saturn"]["retrograde"] is True
        and planets["Rahu"]["retrograde"] is True
        and planets["Ketu"]["retrograde"] is True
    )


def test_planet_house_themes():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

    return all(
        isinstance(planets[planet]["text"], str)
        and len(planets[planet]["text"]) > 0
        for planet in planets
    )


def test_all_zodiac_signs_mapping():
    engine = TharuMagaInterpretationEngine(make_chart())

    expected = {
        "Aries": "මේෂ",
        "Taurus": "වෘෂභ",
        "Gemini": "මිථුන",
        "Cancer": "කටක",
        "Leo": "සිංහ",
        "Virgo": "කන්‍යා",
        "Libra": "තුලා",
        "Scorpio": "වෘශ්චික",
        "Sagittarius": "ධනු",
        "Capricorn": "මකර",
        "Aquarius": "කුම්භ",
        "Pisces": "මීන",
    }

    return all(
        engine._sign_si(sign) == sinhala
        for sign, sinhala in expected.items()
    )


def test_all_house_meanings():
    engine = TharuMagaInterpretationEngine(make_chart())

    return (
        len(engine.HOUSE_MEANINGS) == 12
        and all(
            house in engine.HOUSE_MEANINGS
            for house in range(1, 13)
        )
    )


def test_missing_planet_is_safe():
    chart = make_chart()

    chart["planets"].pop("Mars")

    result = TharuMagaInterpretationEngine(
        chart
    ).generate()

    planets = {
        item["planet"]
        for item in result["planets"]
    }

    return "Mars" not in planets


def test_invalid_planet_entry_is_safe():
    chart = make_chart()

    chart["planets"]["Mars"] = None
    chart["planets"]["Venus"] = "invalid"

    result = TharuMagaInterpretationEngine(
        chart
    ).generate()

    planets = {
        item["planet"]
        for item in result["planets"]
    }

    return (
        "Mars" not in planets
        and "Venus" not in planets
    )


def test_missing_rahu_ketu_is_safe():
    chart = make_chart()

    chart.pop("rahu")
    chart.pop("ketu")

    result = TharuMagaInterpretationEngine(
        chart
    ).generate()

    planets = {
        item["planet"]
        for item in result["planets"]
    }

    return (
        "Rahu" not in planets
        and "Ketu" not in planets
    )


def test_invalid_house_is_safe():
    chart = make_chart()

    chart["planets"]["Mars"]["house"] = "invalid"

    result = TharuMagaInterpretationEngine(
        chart
    ).generate()

    planets = {
        item["planet"]: item
        for item in result["planets"]
    }

    return (
        planets["Mars"]["house"] is None
        and isinstance(planets["Mars"]["text"], str)
    )


def test_complete_interpretation_is_nonempty():
    result = TharuMagaInterpretationEngine(
        make_chart()
    ).generate()

    return (
        isinstance(result["lagna"]["text"], str)
        and len(result["lagna"]["text"]) > 0
        and isinstance(result["moon"]["text"], str)
        and len(result["moon"]["text"]) > 0
        and len(result["planets"]) >= 9
    )


def main():
    print()
    print("THARUMAGA OVERALL CHART INTERPRETATION DEEP AUDIT")
    print()

    tests = [
        ("test_result_contract", test_result_contract),
        ("test_lagna_interpretation", test_lagna_interpretation),
        ("test_moon_interpretation", test_moon_interpretation),
        ("test_all_main_planets_present", test_all_main_planets_present),
        ("test_sinhala_planet_names", test_sinhala_planet_names),
        ("test_planet_sign_mapping", test_planet_sign_mapping),
        ("test_planet_house_mapping", test_planet_house_mapping),
        ("test_retrograde_context", test_retrograde_context),
        ("test_planet_house_themes", test_planet_house_themes),
        ("test_all_zodiac_signs_mapping", test_all_zodiac_signs_mapping),
        ("test_all_house_meanings", test_all_house_meanings),
        ("test_missing_planet_is_safe", test_missing_planet_is_safe),
        ("test_invalid_planet_entry_is_safe", test_invalid_planet_entry_is_safe),
        ("test_missing_rahu_ketu_is_safe", test_missing_rahu_ketu_is_safe),
        ("test_invalid_house_is_safe", test_invalid_house_is_safe),
        ("test_complete_interpretation_is_nonempty", test_complete_interpretation_is_nonempty),
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