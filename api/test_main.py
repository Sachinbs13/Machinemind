from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_predict_with_valid_input_returns_200():
    payload = {
        "machine_id": "TEST001",
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 40.0,
        "tool_wear": 10.0,
        "type": "M",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["machine_id"] == "TEST001"


def test_predict_with_missing_field_returns_422():
    payload = {
        "machine_id": "TEST002",
        "air_temperature": 300.0,
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        # torque is missing on purpose
        "tool_wear": 10.0,
        "type": "M",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_with_wrong_type_returns_422():
    payload = {
        "machine_id": "TEST003",
        "air_temperature": "not_a_number",
        "process_temperature": 310.0,
        "rotational_speed": 1500.0,
        "torque": 40.0,
        "tool_wear": 10.0,
        "type": "M",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_history_returns_a_list_of_records():
    response = client.get("/history?limit=5")
    assert response.status_code == 200

    data = response.json()
    assert "records" in data
    assert isinstance(data["records"], list)