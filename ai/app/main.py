# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import spacy as spacy_c

# from ai.app import app as ai_app
# from frontend.app import app as ui_app
# from backend.app import app as data_app

app = FastAPI()
log = logging.getLogger(__name__)

origins = [
    "http://localhost:8082",
    "http://localhost:8083",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test():
    return {"Hello": "From ml_app"}


# These fake endpoints allow us to encapsulate if we want
# to easily move to micro services
# TODO: add request object
# TODO: add response object
@app.get("/deident/")
async def deident(req):
    res = await spacy_c.deident(req)
    return res
