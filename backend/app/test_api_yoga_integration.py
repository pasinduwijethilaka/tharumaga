"""
API-level regression test for Yoga integration.

This test calls the FastAPI endpoint directly through TestClient, so no
running Uvicorn server is required.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


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


def get_data():
    response = client.post("/api/v1/chart", json=REFERENCE_PAYLOAD)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["success"] is True
    return body["data"]


def test_api_success():
    data = get_data()
    assert "interpretation" in data
    assert "dasha_interpretation" in data
    assert "yogas" in data
    assert "yoga_interpretation" in data


def test_yoga_detection_api_contract():
    data = get_data()
    yoga = data["yogas"]

    assert yoga["engine"] == "TharuMaga Yoga Detection Engine"
    assert yoga["version"] == "1.2"
    assert yoga["count"] == len(yoga["yogas"])

    ids = {item["id"] for item in yoga["yogas"]}
    assert {
        "gaja_kesari",
        "budha_aditya",
        "raja_yoga",
        "dhana_yoga",
    }.issubset(ids)


def test_yoga_interpretation_api_contract():
    data = get_data()
    interpretation = data["yoga_interpretation"]

    assert interpretation["engine"] == "TharuMaga Yoga Interpretation Engine"
    assert interpretation["version"] == "1.0"
    assert interpretation["count"] == len(
        interpretation["interpretations"]
    )

    ids = {item["id"] for item in interpretation["interpretations"]}
    assert {
        "gaja_kesari",
        "budha_aditya",
        "raja_yoga",
        "dhana_yoga",
    }.issubset(ids)


def test_detection_and_interpretation_counts_match():
    data = get_data()
    assert data["yogas"]["count"] == data["yoga_interpretation"]["count"]


def test_existing_interpretation_and_dasha_are_preserved():
    data = get_data()

    assert isinstance(data["interpretation"], dict)
    assert isinstance(data["dasha_interpretation"], dict)
    assert data["interpretation"]
    assert data["dasha_interpretation"]


def test_reference_chart_still_has_libra_lagna():
    data = get_data()
    assert data["lagna"]["sign"] == "Libra"


def run():
    tests = [
        test_api_success,
        test_yoga_detection_api_contract,
        test_yoga_interpretation_api_contract,
        test_detection_and_interpretation_counts_match,
        test_existing_interpretation_and_dasha_are_preserved,
        test_reference_chart_still_has_libra_lagna,
    ]

    passed = 0

    print("=" * 68)
    print("THARUMAGA API + YOGA INTEGRATION REGRESSION TEST")
    print("=" * 68)

    for test in tests:
        try:
            test()
            print("PASS ", test.__name__)
            passed += 1
        except AssertionError as error:
            print("FAIL ", test.__name__, "-", error)

    print("-" * 68)
    print(f"RESULT: {passed}/{len(tests)} regression tests passed")
    print("=" * 68)

    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    run()
