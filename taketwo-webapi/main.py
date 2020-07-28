from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


db = set()


class Flagged(BaseModel):
    user_id: str
    flagged_string: str
    category: str


class Text(BaseModel):
    content: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    return open("template.html").read()


@app.post("/mark")
def update_item(item: Flagged):
    db.add(item.flagged_string)
    return {"status": "success"}


@app.get("/categories")
def read_categories():
    return [
        {"name": "toxic", "colour": "#ff0000", "description": "description for toxic"},
        {
            "name": "abusive",
            "colour": "#ff0000",
            "description": "description for abusive",
        },
        {
            "name": "negative",
            "colour": "#ff0000",
            "description": "description for negative",
        },
        # {"name": "inacurate", "colour": "#ff0000", "description": "description for inacurate"},
    ]


@app.put("/analyse")
def analyse_text(text: Text):
    res = []
    for phrase in db:
        if phrase in text.content:
            res.append(phrase)
    return {"biased": res}
