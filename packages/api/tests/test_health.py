from starlette.testclient import TestClient
from api.main import create_app

app = create_app()
client = TestClient(app)

def test_health_returns_200():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}