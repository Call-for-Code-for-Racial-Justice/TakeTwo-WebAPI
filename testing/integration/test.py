import requests
#example api test

import json
import sys
sys.path.append('../../taketwo-webapi')
from main import app
from main import validate
from main import db
from fastapi.testclient import TestClient

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
    
def comparePayloads(expected: dict, actual: dict):
    assert expected["user_id"] == actual["user_id"], showDiff(str(expected["user_id"]), str(actual["user_id"]))
    assert expected["flagged_string"] == actual["flagged_string"], showDiff(str(expected["flagged_string"]), str(actual["flagged_string"]))
    assert expected["category"] == actual["category"], showDiff(str(expected["category"]), str(actual["category"]))
    assert expected["info"] == actual["info"], showDiff(str(expected["info"]), str(actual["info"]))
    assert expected["url"] == actual["url"], showDiff(str(expected["url"]), str(actual["url"]))

def showDiff(expected: str, actual: str):
    return "Expected: " + expected + ", Actual: " + actual

if __name__ == '__main__':
    test_save_mark()
