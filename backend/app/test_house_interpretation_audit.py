from .interpretation_engine import TharuMagaInterpretationEngine


def make_chart():
    return {
        "lagna": {
            "sign": "Libra",
            "house": 1,
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


def test_all_12_houses_exist():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    assert len(houses) == 12

    found_houses = {
        item["house"]
        for item in houses
    }

    assert found_houses == set(range(1, 13))


def test_all_house_meanings_exist():
    engine = TharuMagaInterpretationEngine(make_chart())

    assert len(engine.HOUSE_MEANINGS) == 12

    for house in range(1, 13):
        assert house in engine.HOUSE_MEANINGS
        assert engine.HOUSE_MEANINGS[house]


def test_house_result_contract():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    for item in houses:
        assert "house" in item
        assert "meaning" in item
        assert "planets" in item
        assert "text" in item

        assert 1 <= item["house"] <= 12
        assert isinstance(item["planets"], list)
        assert item["meaning"]
        assert item["text"]


def test_planets_are_attached_to_correct_houses():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    by_house = {
        item["house"]: item["planets"]
        for item in houses
    }

    assert "සිකුරු" in by_house[2]

    assert "රවි" in by_house[3]
    assert "බුධ" in by_house[3]

    assert "සඳු" in by_house[4]
    assert "කේතු" in by_house[4]

    assert "කුජ" in by_house[5]

    assert "ගුරු" in by_house[7]
    assert "ශනි" in by_house[7]

    assert "රාහු" in by_house[10]


def test_empty_houses_are_safe():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    by_house = {
        item["house"]: item
        for item in houses
    }

    for house in [1, 6, 8, 9, 11, 12]:
        assert by_house[house]["planets"] == []
        assert by_house[house]["text"]


def test_rahu_house_interpretation():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    house_10 = next(
        item for item in houses
        if item["house"] == 10
    )

    assert "රාහු" in house_10["planets"]
    assert "රාහු" in house_10["text"]


def test_ketu_house_interpretation():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    house_4 = next(
        item for item in houses
        if item["house"] == 4
    )

    assert "කේතු" in house_4["planets"]
    assert "කේතු" in house_4["text"]


def test_libra_lagna_house_signs():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()
    houses = engine.interpret_house_lords(houses)

    by_house = {
        item["house"]: item
        for item in houses
    }

    expected_signs = {
        1: "තුලා",
        2: "වෘශ්චික",
        3: "ධනු",
        4: "මකර",
        5: "කුම්භ",
        6: "මීන",
        7: "මේෂ",
        8: "වෘෂභ",
        9: "මිථුන",
        10: "කටක",
        11: "සිංහ",
        12: "කන්‍යා",
    }

    for house, sign in expected_signs.items():
        assert by_house[house]["sign_si"] == sign


def test_libra_lagna_house_lords():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()
    houses = engine.interpret_house_lords(houses)

    by_house = {
        item["house"]: item
        for item in houses
    }

    expected_lords = {
        1: "Venus",
        2: "Mars",
        3: "Jupiter",
        4: "Saturn",
        5: "Saturn",
        6: "Jupiter",
        7: "Mars",
        8: "Venus",
        9: "Mercury",
        10: "Moon",
        11: "Sun",
        12: "Mercury",
    }

    for house, lord in expected_lords.items():
        assert by_house[house]["lord"] == lord


def test_house_lord_placements():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()
    houses = engine.interpret_house_lords(houses)

    by_house = {
        item["house"]: item
        for item in houses
    }

    # Libra Lagna:
    # 1st lord Venus -> 2nd
    assert by_house[1]["lord"] == "Venus"
    assert by_house[1]["lord_house"] == 2

    # 2nd lord Mars -> 5th
    assert by_house[2]["lord"] == "Mars"
    assert by_house[2]["lord_house"] == 5

    # 4th lord Saturn -> 7th
    assert by_house[4]["lord"] == "Saturn"
    assert by_house[4]["lord_house"] == 7

    # 10th lord Moon -> 4th
    assert by_house[10]["lord"] == "Moon"
    assert by_house[10]["lord_house"] == 4


def test_no_absolute_guarantees_in_house_text():
    engine = TharuMagaInterpretationEngine(make_chart())

    houses = engine.interpret_houses()

    forbidden = [
        "අනිවාර්යයෙන්",
        "නියත වශයෙන්",
        "සියයට 100",
        "අනිවාර්ය සාර්ථකත්වය",
        "guaranteed",
        "certainly",
        "100%",
    ]

    for item in houses:
        text = item["text"].lower()

        for phrase in forbidden:
            assert phrase.lower() not in text


def test_empty_chart_is_safe():
    engine = TharuMagaInterpretationEngine({})

    houses = engine.interpret_houses()

    assert isinstance(houses, list)
    assert len(houses) == 12


def test_complete_interpretation_contains_houses():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.generate()

    assert "houses" in result
    assert isinstance(result["houses"], list)
    assert len(result["houses"]) == 12


def run_all():
    tests = [
        test_all_12_houses_exist,
        test_all_house_meanings_exist,
        test_house_result_contract,
        test_planets_are_attached_to_correct_houses,
        test_empty_houses_are_safe,
        test_rahu_house_interpretation,
        test_ketu_house_interpretation,
        test_libra_lagna_house_signs,
        test_libra_lagna_house_lords,
        test_house_lord_placements,
        test_no_absolute_guarantees_in_house_text,
        test_empty_chart_is_safe,
        test_complete_interpretation_contains_houses,
    ]

    print("=" * 68)
    print("THARUMAGA HOUSE INTERPRETATION DEEP AUDIT")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS : {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} audit tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()