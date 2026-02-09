from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict():
    r = client.post("/predict", json={"x": 3})
    assert r.status_code == 200
    assert r.json()["prediction"] == 6
