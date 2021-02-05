from dotenv import load_dotenv
load_dotenv()

import os
import json

from typing import Optional

from fastapi import FastAPI, Depends, FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.responses import HTMLResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx
import base64

import couchdb

import jwt


clear_token = os.getenv("CLEAR_TOKEN")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

client = None
db = None
creds = None

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def retrieve_token(username, password):

    client_id = os.getenv("CLIENT_ID")
    secret = os.getenv("SECRET")
    url = os.getenv("OAUTH_SERVER_URL") + "/token"
    grant_type = "password"

    usrPass = client_id + ":" + secret
    b64Val = base64.b64encode(usrPass.encode()).decode()
    headers = {"accept": "application/json", "Authorization": "Basic %s" % b64Val}

    data = {
        "grant_type": grant_type,
        "username": username,
        "password": password,
        "scope": "all",
    }

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)




def validate(token: str = Depends(oauth2_scheme)):
    res = validate_token_IBM(
        token, os.getenv("OAUTH_SERVER_URL"), os.getenv("CLIENT_ID"), os.getenv("SECRET")
    )
    return res


def validate_token_IBM(token, authURL, clientId, clientSecret=Depends(oauth2_scheme)):
    usrPass = clientId + ":" + clientSecret
    b64Val = base64.b64encode(usrPass.encode()).decode()
    # headers = {'accept': 'application/json', 'Authorization': 'Basic %s' % b64Val}
    headers = {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % b64Val,
    }
    data = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "token": token,
    }
    url = authURL + "/introspect"

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK and response.json()["active"]:
        return jwt.decode(token, options={"verify_signature": False})
    else:
        raise HTTPException(status_code=403, detail="Authorisation failure")


client = couchdb.Server(f'http://{db_username}:{db_password}@{db_host}:{db_port}/')
try: 
    db = client.create(db_name)
except couchdb.PreconditionFailed:
    db = client[db_name]


class Flagged(BaseModel):
    _id: Optional[str]
    user_id: str
    flagged_string: str
    category: str
    info: Optional[str]
    url: str


class Text(BaseModel):
    content: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    return open("template.html").read()


# Get auth token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Gets a token from IBM APP ID, given a username and a password. Depends on OAuth2PasswordRequestForm.
    Parameters
    ----------
    OAuth2PasswordRequestForm.form_data.username: str, required
    OAuth2PasswordRequestForm.form_data.password: str, required
    Returns
    -------
    token: str
    """
    # print(retrieve_token(form_data.username,form_data.password))
    return retrieve_token(form_data.username, form_data.password)


@app.get("/mark")
def get_marks(user: dict = Depends(validate)):
    return list(map(lambda item: dict(item.doc.items()), db.view('_all_docs',include_docs=True)))


@app.post("/mark")
def save_mark(item: Flagged, user: dict = Depends(validate)):
    item.user_id = user["sub"]
    data = item.dict()
    _id, _ = db.save(data)
    return data


@app.put("/mark/{_id}")
def update_mark(_id: str, item: Flagged, user: dict = Depends(validate)):
    doc = db[_id]
    doc["category"] = item.category
    db[doc.id] = doc
    return {"status": "success"}


@app.delete("/mark")
def delete_mark(_id: str, user: dict = Depends(validate)):
    my_document = db[_id]
    my_document.delete()
    return {"status": "success"}


@app.get("/categories")
def read_categories():
    # fmt: off
    return [
        #IBM colour-blindness palette used below https://davidmathlogic.com/colorblind/ 
        {
            "name": "appropriation", 
            "colour": "#648FFF", 
            "description": "To adopt or claim elements of one or more cultures to which you do not belong, consequently causing offence to members of said culture(s) or otherwise achieving some sort of personal gain at the expense of other members of the culture(s)."
        },
        {
            "name": "stereotyping",
            "colour": "#785EF0",
            "description": "To perpetuate a system of beliefs about superficial characteristics of members of a given ethnic group or nationality, their status, society and cultural norms.",
        },
        {
            "name": "under-representation",
            "colour": "#DC267F",
            "description": "To have Insufficient or disproportionately low representation of Black, Indigenous, People of Color (BIPOC) individuals, for example in mediums such as media and TV adverts.",
        },
        {
            "name": "gaslighting", 
            "colour": "#FE6100", 
            "description": "To use tactics, whether by a person or entity, in order to gain more power by making a victim question their reality.  To deny or refuse to see racial bias, which may also include the act of convincing a person that an event/slur/idea is not racist or not as bad as one claims it to be through means of psychological manipulation."
        },
        {
            "name": "racial-slur",
            "colour": "#FFB000",
            "description": "To insult, or use offensive or hurtful language designed to degrade a person because of their race or culture. This is intentional use of words or phrases to speak of or to members of ethnical groups in a derogatory manor. ",
        },
        {
            "name": "othering", 
            "colour": "#5DDB2B", 
            "description": "To label and define a person/group as someone who belongs to a 'socially subordinate' category of society. The practice of othering persons means to use the characteristics of a person's race to exclude and displace such person from the 'superior' social group and separate them from what is classed as normal."
        },
    ]
    # fmt: on


@app.put("/analyse")
def analyse_text(text: Text):
    res = []
    for item in db.view('_all_docs',include_docs=True):
        doc = item.doc
        if doc["flagged_string"] in text.content:
            res.append({"flag" : doc["flagged_string"], "category" : doc["category"], "info" : doc["info"]})
    return {"biased": res}

@app.put("/check")
def check_words(text: Text):
    res = []
    for item in db.view('_all_docs',include_docs=True):
        doc = item.doc
        if doc["category"] == "racial slur" and doc["flagged_string"].lower() in text.content.lower():
            res.append({"flag" : doc["flagged_string"], "category" : doc["category"], "info" : doc["info"]})
    
    line_by_line = []
    for i,l in enumerate(text.content.splitlines(),1):
        for r in res:
            if r["flag"].lower() in l.lower():
                line_by_line.append({
                    "line" : i,
                    "word" : r["flag"],
                    "additional_info": r["info"]
                })

    return line_by_line

