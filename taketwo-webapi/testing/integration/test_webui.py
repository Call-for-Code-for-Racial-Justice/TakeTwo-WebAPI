from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_read_categories():
    url = '/categories'
    resp = client.get(url)

    # Validate status code.
    assert resp.status_code == 200
