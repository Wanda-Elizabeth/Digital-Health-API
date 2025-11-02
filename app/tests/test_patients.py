# tests/test_patients.py
from fastapi.testclient import TestClient
from .conftest import client

def test_create_and_get_patient():
    patient_data = {
        "identifier": "T100",
        "given_name": "Test",
        "family_name": "User",
        "birth_date": "1990-01-01",
        "gender": "other"
    }
    resp = client.post("/api/patients/", json=patient_data)
    assert resp.status_code == 200
    body = resp.json()
    assert body["identifier"] == "T100"
    pid = body["id"]

    get_resp = client.get(f"/api/patients/{pid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["family_name"] == "User"

def test_search_and_delete_patient():
    # Ensure patient exists
    resp = client.post("/api/patients/", json={
        "identifier": "T200",
        "given_name": "Alice",
        "family_name": "Smith",
        "birth_date": "1985-03-20",
        "gender": "female"
    })
    assert resp.status_code == 200

    search = client.get("/api/patients?family_name=Smith")
    assert search.status_code == 200
    results = search.json()
    assert any(p["identifier"] == "T200" for p in results)

    # delete
    pid = [p["id"] for p in results if p["identifier"] == "T200"][0]
    del_resp = client.delete(f"/api/patients/{pid}")
   assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Patient deleted successfully"

    # verify gone
    get_resp = client.get(f"/api/patients/{pid}")
    assert get_resp.status_code == 404
