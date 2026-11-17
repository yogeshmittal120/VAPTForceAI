"""Tests for assessment management endpoints."""


def test_create_and_list_assessment(client):
    payload = {
        "name": "Sample Python API",
        "repository_url": "https://github.com/example/sample-api",
        "scan_types": ["sast", "dependency", "secret"],
    }

    create_response = client.post("/api/v1/assessments", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == payload["name"]
    assert created["status"] == "created"
    assert created["scan_types"] == payload["scan_types"]
    assert created["id"]

    list_response = client.get("/api/v1/assessments")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["id"] == created["id"]


def test_get_unknown_assessment_returns_404(client):
    response = client.get("/api/v1/assessments/not-a-real-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Assessment not found"
