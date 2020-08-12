import os

import json

from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi.responses import HTMLResponse

# from fastapi.middleware.cors import CORSMiddleware

from cloudant.client import Cloudant

app = FastAPI()

clear_token = os.getenv("CLEAR_TOKEN")
db_name = os.getenv("DBNAME")
client = None
db = None
creds = None

if "VCAP_SERVICES" in os.environ:
    creds = json.loads(os.getenv("VCAP_SERVICES"))
    print("Found VCAP_SERVICES")
elif os.path.isfile("vcap-local.json"):
    with open("vcap-local.json") as f:
        creds = json.load(f)
        print("Found local VCAP_SERVICES")

if creds:
    username = creds["username"]
    apikey = creds["apikey"]
    url = creds["url"]
    client = Cloudant.iam(username, apikey, url=url, connect=True)
    db = client.create_database(db_name, throw_on_exists=False)


class Flagged(BaseModel):
    _id: Optional[str]
    user_id: str
    flagged_string: str
    category: str
    url: str


class Text(BaseModel):
    content: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    return open("template.html").read()


@app.get("/mark")
def get_marks():
    return list(map(lambda doc: doc, db))


@app.post("/mark")
def save_mark(item: Flagged):
    data = item.dict()
    if client:
        my_document = db.create_document(data)
        data["_id"] = my_document["_id"]
        return data
    else:
        print("No database")
        return data


@app.put("/mark/{_id}")
def update_mark(_id: str, item: Flagged):
    my_document = db[_id]
    my_document["category"] = item.category
    my_document.save()
    return {"status": "success"}


@app.delete("/mark")
def delete_mark(_id: str):
    my_document = db[_id]
    my_document.delete()
    return {"status": "success"}

if os.path.isfile("vcap-local.json"):
    @app.put("/clear_all")
    def clear_all(confirm: str):
        if confirm == clear_token:
            for doc in db:
                doc.delete()
            return {"status": "success"}
        return {"status": "failed"}


@app.get("/categories")
def read_categories():
    # fmt: off
    return [
        #IBM colour-blindness palette used below https://davidmathlogic.com/colorblind/ 
        {
            "name": "appropriation", 
            "colour": "#648FFF", 
            "description": "description for appropriation"
        },
        {
            "name": "stereotyping",
            "colour": "#785EF0",
            "description": "description for stereotyping",
        },
        {
            "name": "deflection",
            "colour": "#DC267F",
            "description": "description for deflection",
        },
        {
            "name": "gaslighting", 
            "colour": "#FE6100", 
            "description": "description for gaslighting"
        },
        {
            "name": "othering", 
            "colour": "#FFB000", 
            "description": "description for othering"
        },
    ]
    # fmt: on


@app.put("/analyse")
def analyse_text(text: Text):
    res = []
    for doc in db:
        if doc["flagged_string"] in text.content:
            res.append({"flag" : doc["flagged_string"], "category" : doc["category"]})
    return {"biased": res}


# @app.post("/texts")
# def post_texts():

# @app.get("/texts")
# def get_texts():
