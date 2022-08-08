from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_vessels():
    response = client.get("/vessels/")
    assert response.status_code == 200
    assert response.json() != {}

def test_get_vessel_destination_bad_token():
    response = client.get("/destination/{destination}", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200

'''The test passing only once because here is no DB rollback'''
def test_create_vessel():
    response = client.post("/add/",
    headers={"X-Token": "coneofsilence"},
    json={"name": "new", "id": "vessel", "naccsCode": "here","date": "2022-07-27","destination": "Tokyo"},
    )
    assert response.status_code == 200
    assert response.json() == {"name": "new", "id": "vessel", "naccsCode": "here","date": "2022-07-27","destination": "Tokyo"}

def test_create_vessel_bad_token():
    response = client.post("/add/",
    headers={"X-Token": "badkey"},)
    assert response.status_code == 422
   
