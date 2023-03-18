import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import os
import sys

sys.path.append(".")

from .schema.base.messages._Request import _Request
from .schema.base.messages._Response import _Response

from .controllers import document as document_c
from .services.utils import cast_to_class
from .emitter import emitter
from pyee import EventEmitter

app = FastAPI()
# ee = emitter
log = logging.getLogger(__name__)

# ---------------------------------------------------#
# DEV
# ---------------------------------------------------#
if os.environ["ENV"] == "DEV":
    origins = [
        f"http://{os.environ['WEB_SERVICE_DOMAIN']}",
        f"http://{os.environ['WEB_SERVICE_DOMAIN']}:{os.environ['WEB_SERVICE_PORT']}",
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# ---------------------------------------------------#
# END DEV
# ---------------------------------------------------#

from fastapi_websocket_pubsub import PubSubClient
import asyncio


async def on_events(data, topic):
    print(f"running callback for {topic}!")


async def _init():

    # await document_c.subscribe()
    return True


@app.on_event("startup")
async def startup():
    await _init()


@app.get("/")
def test():
    return {"Hello": "From ml_app"}


@app.get("/test_training")
async def test_training():
    _res = await document_c.train_model()
    return _res


# TODO: log the round trip on this server
@app.post("/deID", response_class=JSONResponse)
async def deID(req: Request):
    req_data = await req.json()
    _req = _Request.parse_obj(req_data)
    res = await document_c.deID(_req)

    return res


# no longer supported.  Handled with websockets
@app.put("/deID", response_class=JSONResponse)
async def deID(req: Request):
    # TODO: logic to utilize deidentification updates from the UI via a controller
    # req_data = await req.json()

    # _req = _Request.parse_obj(req_data)
    # _res = await document_c.update_deID(_req)

    # return _res
    return {"message": "no longer supported"}
