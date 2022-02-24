import requests
#example api test

import json
import sys
sys.path.append('../../taketwo-webapi')
sys.path.append('../util')
from main import app
from main import validate
from main import db
from fastapi.testclient import TestClient
from testutil import comparePayloads
import unittest

def override_validate():
    return {"sub": 'test'}

app.dependency_overrides[validate] = override_validate

def test_save_mark():
    url = '/mark'
    
    # Additional headers.
    headers = {'Content-Type': 'application/json' } 

    # Body
    payload = {'user_id': "test", 'flagged_string': "test string", 'category': "stereotyping", 'info': "none", 'url': "example.com"}
    
    client = TestClient(app)
    # convert dict to json by json.dumps() for body data. 
    resp = client.post(url, headers=headers, data=json.dumps(payload,indent=4))       
    
    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200, "Unexpected status code. Was: " + str(resp.status_code)
    resp_body = resp.json()
    assert resp_body['url'] == 'example.com', "Unexpected url. Was: " + resp_body['url']

    #make sure payload stored properly
    storedPayload = db.get(resp_body["_id"])
    comparePayloads(payload, storedPayload)
    
    # print response full body as text
    print(resp.text)

if __name__ == '__main__':
    test_save_mark()
