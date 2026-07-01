from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_positive():
    r = client.post("/predict", json={"text": "I love this, it is great and wonderful"})
    assert r.status_code == 200
    assert r.json()["sentiment"] == "positive"


def test_predict_negative():
    r = client.post("/predict", json={"text": "This is terrible, awful and bad"})
    assert r.status_code == 200
    assert r.json()["sentiment"] == "negative"


def test_predict_neutral():
    r = client.post("/predict", json={"text": "the cat sat on the table"})
    assert r.status_code == 200
    assert r.json()["sentiment"] == "neutral"


def test_metrics_exposed():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_request_duration_seconds" in r.text
