from fastapi.testclient import TestClient
from .conftest import client

def test_create_encounter_and_list():
    # create patient
    patient = {
        "identifier": "T300",
        "given_name": "Enc",
        "family_name": "Tester",
        "birth_date": "1991-04-05",
        "gender": "male"
    }
    p = client.post("/api/patients/", json=patient).json()
    pid = p["id"]

    enc = {
        "patient_id": pid,
        "start": "2025-10-31T08:00:00Z",
        "end": "2025-10-31T09:00:00Z",
        "encounter_class": "outpatient"
    }
    resp = client.post("/api/encounters/", json=enc)
    assert resp.status_code == 200
    body = resp.json()
    assert body["patient_id"] == pid

    # list encounters
    list_resp = client.get(f"/api/encounters/patient/{pid}")
    assert list_resp.status_code == 200
    arr = list_resp.json()
   assert isinstance(arr, list)
    assert any(e["encounter_class"] == "outpatient" for e in arr)
