from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_post_headers_body_json():
    url = '/mark'

    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {'user_id': "test", 'flagged_string': "test string", 'category': "stereotyping", 'info': "none",
               'url': "example.com"}

    resp = client.post(url, headers=headers, json=payload)

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['url'] == 'example.com'

    # print response full body as text
    #print(resp.text)