from .interpretation_engine import TharuMagaInterpretationEngine


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
            "Moon": {
                "sign": "Capricorn",
                "house": 4,
            }
        },
    }


def test_lagna_result_contract():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_lagna()

    assert isinstance(result, dict)
    assert "title" in result
    assert "sign" in result
    assert "nakshatra" in result
    assert "text" in result

    assert result["title"]
    assert result["sign"]
    assert result["nakshatra"]
    assert result["text"]


def test_lagna_sign_sinhala_mapping():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_lagna()

    assert result["sign"] == "තුලා"


def test_lagna_nakshatra_is_returned():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_lagna()

    assert result["nakshatra"] == "Vishakha"


def test_lagna_text_contains_sign():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_lagna()

    assert "තුලා" in result["text"]


def test_lagna_text_is_interpretive_not_absolute():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.interpret_lagna()

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
            "lagna": {
                "sign": sign,
                "nakshatra": {
                    "name": "Test Nakshatra",
                },
            }
        }

        engine = TharuMagaInterpretationEngine(chart)
        result = engine.interpret_lagna()

        assert result["sign"] == expected_si


def test_missing_lagna_is_safe():
    engine = TharuMagaInterpretationEngine({})

    result = engine.interpret_lagna()

    assert isinstance(result, dict)
    assert result["sign"] == "-"
    assert result["nakshatra"] == "-"
    assert result["text"]


def test_missing_nakshatra_is_safe():
    chart = {
        "lagna": {
            "sign": "Libra",
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_lagna()

    assert result["sign"] == "තුලා"
    assert result["nakshatra"] == "-"
    assert result["text"]


def test_string_nakshatra_is_safe():
    chart = {
        "lagna": {
            "sign": "Libra",
            "nakshatra": "Vishakha",
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_lagna()

    assert result["nakshatra"] == "Vishakha"


def test_invalid_nakshatra_data_is_safe():
    chart = {
        "lagna": {
            "sign": "Libra",
            "nakshatra": 12345,
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_lagna()

    assert result["nakshatra"] == "12345"
    assert result["text"]


def test_unknown_sign_is_safe():
    chart = {
        "lagna": {
            "sign": "UnknownSign",
            "nakshatra": {
                "name": "Vishakha",
            },
        }
    }

    engine = TharuMagaInterpretationEngine(chart)

    result = engine.interpret_lagna()

    assert result["sign"] == "UnknownSign"
    assert result["nakshatra"] == "Vishakha"
    assert result["text"]


def test_complete_interpretation_contains_lagna():
    engine = TharuMagaInterpretationEngine(make_chart())

    result = engine.generate()

    assert "lagna" in result
    assert isinstance(result["lagna"], dict)

    assert result["lagna"]["sign"] == "තුලා"
    assert result["lagna"]["nakshatra"] == "Vishakha"


def run_all():
    tests = [
        test_lagna_result_contract,
        test_lagna_sign_sinhala_mapping,
        test_lagna_nakshatra_is_returned,
        test_lagna_text_contains_sign,
        test_lagna_text_is_interpretive_not_absolute,
        test_all_zodiac_signs_map_correctly,
        test_missing_lagna_is_safe,
        test_missing_nakshatra_is_safe,
        test_string_nakshatra_is_safe,
        test_invalid_nakshatra_data_is_safe,
        test_unknown_sign_is_safe,
        test_complete_interpretation_contains_lagna,
    ]

    print("=" * 68)
    print("THARUMAGA LAGNA INTERPRETATION DEEP AUDIT")
    print("=" * 68)

    for test in tests:
        test()
        print(f"PASS : {test.__name__}")

    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} audit tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()