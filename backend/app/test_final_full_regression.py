from backend.app.astrology_engine import TharuMagaEngine
from backend.app.interpretation_engine import TharuMagaInterpretationEngine
from backend.app.dasha_interpretation_engine import (
    TharuMagaDashaInterpretationEngine,
)
from backend.app.yoga_detection_engine import TharuMagaYogaEngine
from backend.app.yoga_interpretation_engine import (
    TharuMagaYogaInterpretationEngine,
)


REFERENCE_PAYLOAD = {
    "day": 10,
    "month": 1,
    "year": 2000,
    "hour": 2,
    "minute": 25,
    "second": 0,
    "latitude": 6.9271,
    "longitude": 79.8612,
    "timezone": "Asia/Colombo",
    "place": "Colombo, Sri Lanka",
}


def build_chart():
    return TharuMagaEngine(**REFERENCE_PAYLOAD).calculate()


def check(name, condition):
    if condition:
        print(f"PASS : {name}")
        return True

    print(f"FAIL : {name}")
    return False


def test_engine_core():
    chart = build_chart()

    return (
        chart["lagna"]["sign"] == "Libra"
        and chart["planets"]["Sun"]["sign"] == "Sagittarius"
        and chart["planets"]["Moon"]["sign"] == "Capricorn"
        and chart["planets"]["Mars"]["sign"] == "Aquarius"
        and chart["planets"]["Mercury"]["sign"] == "Sagittarius"
        and chart["planets"]["Jupiter"]["sign"] == "Aries"
        and chart["planets"]["Venus"]["sign"] == "Scorpio"
        and chart["planets"]["Saturn"]["sign"] == "Aries"
    )


def test_whole_sign_houses():
    chart = build_chart()
    planets = chart["planets"]

    return (
        planets["Venus"]["house"] == 2
        and planets["Sun"]["house"] == 3
        and planets["Mercury"]["house"] == 3
        and planets["Moon"]["house"] == 4
        and planets["Mars"]["house"] == 5
        and planets["Jupiter"]["house"] == 7
        and planets["Saturn"]["house"] == 7
        and chart["rahu"]["house"] == 10
        and chart["ketu"]["house"] == 4
    )


def test_rahu_ketu():
    chart = build_chart()

    rahu = chart["rahu"]["longitude"]
    ketu = chart["ketu"]["longitude"]

    difference = abs((ketu - rahu) % 360)

    return (
        abs(difference - 180) < 1e-9
        or abs(difference - 180) < 1e-6
    )


def test_result_contract():
    chart = build_chart()

    required = {
        "engine",
        "birth",
        "lagna",
        "planets",
        "rahu",
        "ketu",
        "d1",
        "moon_nakshatra",
        "birth_mahadasha",
        "dasha",
    }

    return required.issubset(chart.keys())


def test_interpretation():
    chart = build_chart()
    result = TharuMagaInterpretationEngine(chart).generate()

    return (
        isinstance(result, dict)
        and isinstance(result["lagna"], dict)
        and isinstance(result["moon"], dict)
        and isinstance(result["planets"], list)
        and len(result["planets"]) >= 9
    )


def test_dasha():
    chart = build_chart()

    result = TharuMagaDashaInterpretationEngine(
        chart
    ).generate()

    return (
        result["available"] is True
        and result["current"]["mahadasha"] is not None
        and result["current"]["antardasha"] is not None
        and result["current"]["pratyantardasha"] is not None
        and result["combined_text"]
    )


def test_yoga_detection():
    chart = build_chart()
    result = TharuMagaYogaEngine(chart).generate()

    ids = {
        yoga["id"]
        for yoga in result["yogas"]
    }

    return (
        result["count"] == len(result["yogas"])
        and {
            "gaja_kesari",
            "budha_aditya",
            "raja_yoga",
            "dhana_yoga",
        }.issubset(ids)
    )


def test_yoga_interpretation():
    chart = build_chart()

    detected = TharuMagaYogaEngine(chart).generate()
    result = TharuMagaYogaInterpretationEngine(
        detected
    ).generate()

    ids = {
        item["id"]
        for item in result["interpretations"]
    }

    return (
        result["count"] == len(result["interpretations"])
        and {
            "gaja_kesari",
            "budha_aditya",
            "raja_yoga",
            "dhana_yoga",
        }.issubset(ids)
    )


def test_full_pipeline():
    chart = build_chart()

    interpretation = TharuMagaInterpretationEngine(
        chart
    ).generate()

    dasha = TharuMagaDashaInterpretationEngine(
        chart
    ).generate()

    yogas = TharuMagaYogaEngine(chart).generate()

    yoga_interpretation = TharuMagaYogaInterpretationEngine(
        yogas
    ).generate()

    return (
        chart["lagna"]["sign"] == "Libra"
        and interpretation
        and dasha["available"] is True
        and yogas["count"] > 0
        and yoga_interpretation["count"] == yogas["count"]
    )


def main():
    print()
    print("=" * 68)
    print("THARUMAGA FINAL FULL REGRESSION AUDIT")
    print("=" * 68)
    print()

    tests = [
        ("test_engine_core", test_engine_core),
        ("test_whole_sign_houses", test_whole_sign_houses),
        ("test_rahu_ketu", test_rahu_ketu),
        ("test_result_contract", test_result_contract),
        ("test_interpretation", test_interpretation),
        ("test_dasha", test_dasha),
        ("test_yoga_detection", test_yoga_detection),
        ("test_yoga_interpretation", test_yoga_interpretation),
        ("test_full_pipeline", test_full_pipeline),
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
    print("-" * 68)
    print(f"RESULT: {passed}/{len(tests)} final regression tests passed")
    print("=" * 68)

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    main()