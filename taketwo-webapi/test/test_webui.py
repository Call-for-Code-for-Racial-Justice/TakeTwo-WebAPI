from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_read_categories():
    url = '/categories'
    resp = client.get(url)

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200

    # print response full body as text
    print(resp.text)