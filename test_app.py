from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_session
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.rollback()
        db.close()

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

'''The test passing only once because here is no DB rollback'''
def test_create_vessel():
    response = client.post(
        "/add/",
        json={"name": "shippio", "id": "vessel", "naccsCode": "company","date": "12-05-7","destination": "Osaka"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "shippio"
    assert "destination" in data
    vessel_destination= data["destination"]

    response = client.get(f"/destination/{vessel_destination}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "shippio"
    assert data["destination"] == vessel_destination


