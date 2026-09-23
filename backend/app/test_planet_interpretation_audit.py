from .interpretation_engine import TharuMagaInterpretationEngine


PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]


def make_chart():
    planets = {}

    for index, planet in enumerate(PLANETS):
        planets[planet] = {
            "sign": "Aries",
            "house": (index % 12) + 1,
            "retrograde": False,
        }

    return {
        "lagna": {
            "sign": "Aries",
            "house": 1,
        },
        "planets": planets,
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


def test_all_main_planets_have_names():
    engine = TharuMagaInterpretationEngine(make_chart())

    for planet in PLANETS:
        assert planet in engine.PLANET_NAMES_SI
        assert engine.PLANET_NAMES_SI[planet]


def test_all_main_planets_have_12_house_themes():
    engine = TharuMagaInterpretationEngine(make_chart())

    for planet in PLANETS:
        assert planet in engine.PLANET_HOUSE_THEMES

        themes = engine.PLANET_HOUSE_THEMES[planet]

        assert isinstance(themes, dict)
        assert set(themes.keys()) == set(range(1, 13))

        for house in range(1, 13):
            assert themes[house]
            assert isinstance(themes[house], str)


def test_planet_interpretation_returns_all_planets():
    engine = TharuMagaInterpretationEngine(make_chart())

    results = engine.interpret_planets()

    found = {
        item["planet"]
        for item in results
        if isinstance(item, dict)
    }

    for planet in PLANETS:
        assert planet in found


def test_planet_result_contract():
    engine = TharuMagaInterpretationEngine(make_chart())

    results = engine.interpret_planets()

    for item in results:
        assert "planet" in item
        assert "planet_si" in item
        assert "sign" in item
        assert "house" in item
        assert "retrograde" in item
        assert "text" in item

        assert item["planet"]
        assert item["planet_si"]
        assert item["text"]


def test_rahu_is_interpreted():
    engine = TharuMagaInterpretationEngine(make_chart())

    results = engine.interpret_planets()

    rahu = next(
        item for item in results
        if item["planet"] == "Rahu"
    )

    assert rahu["planet_si"] == "රාහු"
    assert rahu["house"] == 10
    assert rahu["text"]


def test_ketu_is_interpreted():
    engine = TharuMagaInterpretationEngine(make_chart())

    results = engine.interpret_planets()

    ketu = next(
        item for item in results
        if item["planet"] == "Ketu"
    )

    assert ketu["planet_si"] == "කේතු"
    assert ketu["house"] == 4
    assert ketu["text"]


def test_no_absolute_guarantees_in_planet_themes():
    engine = TharuMagaInterpretationEngine(make_chart())

    forbidden = [
        "අනිවාර්යයෙන්",
        "නියත වශයෙන්",
        "සියයට 100",
        "අනිවාර්ය සාර්ථකත්වය",
        "guaranteed",
        "certainly",
        "100%",
    ]

    for planet in PLANETS:
        for house in range(1, 13):
            text = engine.PLANET_HOUSE_THEMES[planet][house].lower()

            for phrase in forbidden:
                assert phrase.lower() not in text


def test_empty_chart_is_safe():
    engine = TharuMagaInterpretationEngine({})

    results = engine.interpret_planets()

    assert isinstance(results, list)


def test_missing_planet_data_is_safe():
    chart = {
        "planets": {
            "Sun": {
                "sign": "Aries",
                "house": 1,
            },
            "Moon": None,
            "Mars": "invalid",
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    results = engine.interpret_planets()

    assert isinstance(results, list)

    sun = next(
        item for item in results
        if item["planet"] == "Sun"
    )

    assert sun["house"] == 1
    assert sun["text"]


def test_complete_interpretation_contract():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.generate()

    assert "lagna" in result
    assert "moon" in result
    assert "planets" in result
    assert "houses" in result

    assert isinstance(result["planets"], list)
    assert isinstance(result["houses"], list)


def run_all():
    tests = [
        test_all_main_planets_have_names,
        test_all_main_planets_have_12_house_themes,
        test_planet_interpretation_returns_all_planets,
        test_planet_result_contract,
        test_rahu_is_interpreted,
        test_ketu_is_interpreted,
        test_no_absolute_guarantees_in_planet_themes,
        test_empty_chart_is_safe,
        test_missing_planet_data_is_safe,
        test_complete_interpretation_contract,
    ]

    print("=" * 68)
    print("THARUMAGA PLANET INTERPRETATION DEEP AUDIT")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS : {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} audit tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()