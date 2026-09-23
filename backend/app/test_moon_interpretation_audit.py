from .interpretation_engine import TharuMagaInterpretationEngine


def make_chart():
    return {
        "lagna": {
            "sign": "Libra",
        },
        "planets": {
            "Moon": {
                "sign": "Capricorn",
                "house": 4,
            }
        },
    }


def test_moon_result_contract():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    assert isinstance(result, dict)

    assert "title" in result
    assert "sign" in result
    assert "house" in result
    assert "text" in result

    assert result["title"]
    assert result["sign"]
    assert result["house"] == 4
    assert result["text"]


def test_moon_sign_sinhala_mapping():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    assert result["sign"] == "මකර"


def test_moon_house_is_returned():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    assert result["house"] == 4


def test_moon_text_contains_sign_and_house():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    assert "මකර" in result["text"]
    assert "4" in result["text"]


def test_moon_uses_house_meaning():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    expected_meaning = engine.HOUSE_MEANINGS[4]

    assert expected_meaning in result["text"]


def test_moon_interpretation_is_cautious():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_moon()

    forbidden = [
        "අනිවාර්යයෙන්",
        "නියත වශයෙන්",
        "සියයට 100",
        "අනිවාර්ය සාර්ථකත්වය",
        "guaranteed",
        "certainly",
        "100%",
    ]

    text = result["text"].lower()

    for phrase in forbidden:
        assert phrase.lower() not in text


def test_all_zodiac_signs_map_correctly():
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

    for sign, expected_si in expected.items():

        chart = {
            "planets": {
                "Moon": {
                    "sign": sign,
                    "house": 1,
                }
            }
        }

        engine = TharuMagaInterpretationEngine(chart)

        result = engine.interpret_moon()

        assert result["sign"] == expected_si


def test_all_valid_houses_are_safe():
    for house in range(1, 13):

        chart = {
            "planets": {
                "Moon": {
                    "sign": "Capricorn",
                    "house": house,
                }
            }
        }

        engine = TharuMagaInterpretationEngine(chart)

        result = engine.interpret_moon()

        assert result["house"] == house
        assert result["text"]


def test_missing_moon_is_safe():
    engine = TharuMagaInterpretationEngine({})

    result = engine.interpret_moon()

    assert isinstance(result, dict)
    assert result["sign"] == "-"
    assert result["house"] is None
    assert result["text"]


def test_missing_moon_sign_is_safe():
    chart = {
        "planets": {
            "Moon": {
                "house": 4,
            }
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_moon()

    assert result["sign"] == "-"
    assert result["house"] == 4
    assert result["text"]


def test_missing_moon_house_is_safe():
    chart = {
        "planets": {
            "Moon": {
                "sign": "Capricorn",
            }
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_moon()

    assert result["sign"] == "මකර"
    assert result["house"] is None
    assert result["text"]


def test_invalid_moon_data_is_safe():
    chart = {
        "planets": {
            "Moon": "invalid",
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_moon()

    assert isinstance(result, dict)
    assert result["sign"] == "-"
    assert result["house"] is None
    assert result["text"]


def test_invalid_house_value_is_safe():
    chart = {
        "planets": {
            "Moon": {
                "sign": "Capricorn",
                "house": "invalid",
            }
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_moon()

    assert result["sign"] == "මකර"
    assert result["house"] is None
    assert result["text"]


def test_complete_interpretation_contains_moon():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.generate()

    assert "moon" in result
    assert isinstance(result["moon"], dict)

    assert result["moon"]["sign"] == "මකර"
    assert result["moon"]["house"] == 4


def run_all():
    tests = [
        test_moon_result_contract,
        test_moon_sign_sinhala_mapping,
        test_moon_house_is_returned,
        test_moon_text_contains_sign_and_house,
        test_moon_uses_house_meaning,
        test_moon_interpretation_is_cautious,
        test_all_zodiac_signs_map_correctly,
        test_all_valid_houses_are_safe,
        test_missing_moon_is_safe,
        test_missing_moon_sign_is_safe,
        test_missing_moon_house_is_safe,
        test_invalid_moon_data_is_safe,
        test_invalid_house_value_is_safe,
        test_complete_interpretation_contains_moon,
    ]

    print("=" * 68)
    print("THARUMAGA MOON INTERPRETATION DEEP AUDIT")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS : {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} audit tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()