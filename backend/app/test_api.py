from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)


# =========================================================
# TEST 1 — Valid Chart
# =========================================================
def test_valid_chart():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 15,
            "month": 5,
            "year": 1995,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 6.9271,
            "longitude": 79.8612,
            "timezone": "Asia/Colombo",
            "place": "Colombo, Sri Lanka"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    # Lagna
    assert data["data"]["lagna"]["sign"] == "Cancer"

    # Moon Nakshatra
    assert data["data"]["moon_nakshatra"]["name"] == "Anuradha"

    # Birth Mahadasha
    assert data["data"]["birth_mahadasha"]["lord"] == "Saturn"

    print("✓ Valid chart test passed")


# =========================================================
# TEST 2 — Invalid Latitude
# =========================================================
def test_invalid_latitude():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 15,
            "month": 5,
            "year": 1995,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 100,
            "longitude": 79.8612,
            "timezone": "Asia/Colombo",
            "place": "Colombo, Sri Lanka"
        }
    )

    assert response.status_code == 422

    print("✓ Invalid latitude test passed")


# =========================================================
# TEST 3 — Invalid Longitude
# =========================================================
def test_invalid_longitude():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 15,
            "month": 5,
            "year": 1995,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 6.9271,
            "longitude": 200,
            "timezone": "Asia/Colombo",
            "place": "Colombo, Sri Lanka"
        }
    )

    assert response.status_code == 422

    print("✓ Invalid longitude test passed")


# =========================================================
# TEST 4 — Missing Optional Place Field
# =========================================================
def test_optional_place():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 15,
            "month": 5,
            "year": 1995,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 6.9271,
            "longitude": 79.8612,
            "timezone": "Asia/Colombo"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["birth"]["place"] == ""

    print("✓ Optional place field test passed")


# =========================================================
# TEST 5 — Missing Required Field
# =========================================================
def test_missing_required_field():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 15,
            "month": 5,
            "year": 1995,
            "hour": 10,
            "minute": 30,
            "second": 0,
            "latitude": 6.9271,
            "longitude": 79.8612
            # timezone intentionally missing
        }
    )

    assert response.status_code == 422

    print("✓ Missing required field test passed")


# =========================================================
# TEST 6 — Different Birth Data
# =========================================================
def test_different_birth_data():
    response = client.post(
        "/api/v1/chart",
        json={
            "day": 20,
            "month": 8,
            "year": 2000,
            "hour": 14,
            "minute": 15,
            "second": 0,
            "latitude": 6.9271,
            "longitude": 79.8612,
            "timezone": "Asia/Colombo",
            "place": "Colombo, Sri Lanka"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    # Different birth data should produce a different chart
    assert data["data"]["birth"]["date"] == "2000-08-20"
    assert data["data"]["birth"]["local_time"] == "14:15:00"

    print("✓ Different birth data test passed")


# =========================================================
# RUN ALL TESTS
# =========================================================
if __name__ == "__main__":

    print()
    print("========================================")
    print("       THARUMAGA API TEST SUITE")
    print("========================================")
    print()

    test_valid_chart()

    test_invalid_latitude()

    test_invalid_longitude()

    test_optional_place()

    test_missing_required_field()

    test_different_birth_data()

    print()
    print("========================================")
    print("       ✓ ALL API TESTS PASSED")
    print("========================================")
    print()