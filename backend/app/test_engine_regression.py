"""
TharuMaga Astrology Engine Regression Tests

Run from project root:
    python -m pytest backend\\app\\test_engine_regression.py -q

Or:
    python backend\\app\\test_engine_regression.py
"""

from math import isclose
from backend.app.astrology_engine import TharuMagaEngine


CHART_2000 = {
    "day": 10, "month": 1, "year": 2000,
    "hour": 2, "minute": 25, "second": 0,
    "latitude": 6.9271, "longitude": 79.8612,
    "timezone": "Asia/Colombo",
    "place": "Colombo, Sri Lanka",
}

CHART_1995 = {
    "day": 15, "month": 5, "year": 1995,
    "hour": 10, "minute": 30, "second": 0,
    "latitude": 6.9271, "longitude": 79.8612,
    "timezone": "Asia/Colombo",
    "place": "Colombo, Sri Lanka",
}


def chart(details):
    return TharuMagaEngine(**details).calculate()


def close(actual, expected, tol=1e-8):
    assert isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=tol), (
        f"Expected {expected}, got {actual}"
    )


def test_engine_contract():
    r = chart(CHART_2000)
    assert r["engine"]["name"] == "TharuMaga"
    assert r["engine"]["zodiac"] == "Sidereal"
    assert r["engine"]["ayanamsa"] == "Lahiri"
    assert r["engine"]["rahu"] == "True Node"
    assert r["engine"]["ketu"] == "180° opposite Rahu"
    assert r["engine"]["house_system"] == "Whole Sign"
    assert r["engine"]["dasha_system"] == "Vimshottari"


def test_historical_colombo_timezone():
    r = chart(CHART_2000)
    assert r["birth"]["local_time"] == "02:25:00"
    assert r["birth"]["timezone"] == "Asia/Colombo"
    assert r["birth"]["utc"] == "2000-01-09 20:25:00"


def test_2000_lagna():
    r = chart(CHART_2000)
    assert r["lagna"]["sign"] == "Libra"
    assert r["lagna"]["sign_index"] == 6
    assert r["lagna"]["nakshatra"]["name"] == "Vishakha"
    assert r["lagna"]["nakshatra"]["lord"] == "Jupiter"
    assert r["lagna"]["nakshatra"]["pada"] == 1
    close(r["lagna"]["longitude"], 201.36121188734143)


def test_2000_planet_signs_and_houses():
    p = chart(CHART_2000)["planets"]
    expected = {
        "Sun": ("Sagittarius", 3),
        "Moon": ("Capricorn", 4),
        "Mars": ("Aquarius", 5),
        "Mercury": ("Sagittarius", 3),
        "Jupiter": ("Aries", 7),
        "Venus": ("Scorpio", 2),
        "Saturn": ("Aries", 7),
    }
    for planet, (sign, house) in expected.items():
        assert p[planet]["sign"] == sign
        assert p[planet]["house"] == house


def test_rahu_ketu():
    r = chart(CHART_2000)
    assert r["rahu"]["sign"] == "Cancer"
    assert r["rahu"]["house"] == 10
    assert r["ketu"]["sign"] == "Capricorn"
    assert r["ketu"]["house"] == 4
    separation = (r["ketu"]["longitude"] - r["rahu"]["longitude"]) % 360
    close(separation, 180.0, 1e-10)


def test_2000_nakshatras():
    p = chart(CHART_2000)["planets"]
    expected = {
        "Sun": ("Purva Ashadha", "Venus", 4),
        "Moon": ("Dhanishta", "Mars", 2),
        "Mars": ("Shatabhisha", "Rahu", 2),
        "Mercury": ("Purva Ashadha", "Venus", 3),
        "Jupiter": ("Ashwini", "Ketu", 1),
        "Venus": ("Jyeshtha", "Mercury", 1),
        "Saturn": ("Bharani", "Venus", 1),
    }
    for planet, (nak, lord, pada) in expected.items():
        n = p[planet]["nakshatra"]
        assert n["name"] == nak
        assert n["lord"] == lord
        assert n["pada"] == pada


def test_1995_reference_chart():
    r = chart(CHART_1995)
    assert r["birth"]["utc"] == "1995-05-15 05:00:00"
    assert r["lagna"]["sign"] == "Cancer"
    assert r["lagna"]["nakshatra"]["name"] == "Pushya"
    assert r["lagna"]["nakshatra"]["lord"] == "Saturn"
    assert r["lagna"]["nakshatra"]["pada"] == 1

    p = r["planets"]
    assert p["Moon"]["sign"] == "Scorpio"
    assert p["Moon"]["house"] == 5
    assert p["Moon"]["nakshatra"]["name"] == "Anuradha"
    assert p["Moon"]["nakshatra"]["lord"] == "Saturn"
    assert p["Moon"]["nakshatra"]["pada"] == 1
    assert p["Sun"]["sign"] == "Taurus"
    assert p["Sun"]["house"] == 11
    assert p["Mars"]["sign"] == "Leo"
    assert p["Mars"]["house"] == 2
    assert p["Jupiter"]["sign"] == "Scorpio"
    assert p["Jupiter"]["house"] == 5
    assert p["Saturn"]["sign"] == "Aquarius"
    assert p["Saturn"]["house"] == 8


def test_whole_sign_relationships():
    r = chart(CHART_2000)
    p = r["planets"]
    assert p["Venus"]["house"] == 2
    assert p["Sun"]["house"] == 3
    assert p["Mercury"]["house"] == 3
    assert p["Moon"]["house"] == 4
    assert p["Mars"]["house"] == 5
    assert p["Jupiter"]["house"] == 7
    assert p["Saturn"]["house"] == 7
    assert r["rahu"]["house"] == 10
    assert r["ketu"]["house"] == 4


def test_dasha_sequence_and_120_year_cycle():
    d = chart(CHART_2000)["dasha"]
    assert len(d) == 9

    # The sequence starts from the birth Mahadasha lord.
    # For this chart, Moon is in Dhanishta, whose lord is Mars.
    assert [x["lord"] for x in d] == [
        "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
        "Ketu", "Venus", "Sun", "Moon"
    ]

    # The first Mahadasha is only the remaining portion at birth,
    # so the displayed "years" values do not sum to the full 120-year
    # Vimshottari cycle. Verify the complete lord cycle separately.
    full_years = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17,
    }
    assert sum(full_years.values()) == 120
    assert float(d[0]["years"]) < full_years["Mars"]
    for item in d[1:]:
        assert float(item["years"]) == full_years[item["lord"]]


def test_dasha_nested_structure():
    for maha in chart(CHART_2000)["dasha"]:
        assert len(maha["antardasha"]) == 9
        for antara in maha["antardasha"]:
            assert len(antara["pratyantardasha"]) == 9


def test_2000_birth_mahadasha():
    assert chart(CHART_2000)["birth_mahadasha"]["lord"] == "Mars"


def test_result_contract():
    r = chart(CHART_2000)
    for key in (
        "engine", "birth", "lagna", "planets", "rahu", "ketu",
        "d1", "moon_nakshatra", "birth_mahadasha", "dasha"
    ):
        assert key in r
    assert isinstance(r["birth"]["utc"], str)


def run_all():
    tests = [
        test_engine_contract,
        test_historical_colombo_timezone,
        test_2000_lagna,
        test_2000_planet_signs_and_houses,
        test_rahu_ketu,
        test_2000_nakshatras,
        test_1995_reference_chart,
        test_whole_sign_relationships,
        test_dasha_sequence_and_120_year_cycle,
        test_dasha_nested_structure,
        test_2000_birth_mahadasha,
        test_result_contract,
    ]
    print("=" * 68)
    print("THARUMAGA ASTROLOGY ENGINE REGRESSION TEST")
    print("=" * 68)
    for test in tests:
        test()
        print(f"PASS  {test.__name__}")
    print("-" * 68)
    print(f"RESULT: {len(tests)}/{len(tests)} regression tests passed")
    print("=" * 68)


if __name__ == "__main__":
    run_all()