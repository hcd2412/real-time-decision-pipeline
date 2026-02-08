from fastapi.testclient import TestClient
from rtp.app.main import app


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

