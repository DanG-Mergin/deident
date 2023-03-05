import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import os
import sys

sys.path.append(".")
from .schema.messages.inbound.DeIDRequest import DeIDRequest
from .schema.messages.outbound.DeIDResponse import DeIDResponse

from .controllers import spacy as spacy_c, feedback as feedback_c
from .services.utils import cast_to_class

# from ai.app import app as ai_app
# from frontend.app import app as ui_app
# from backend.app import app as data_app

app = FastAPI()
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


@app.get("/")
def test():
    return {"Hello": "From ml_app"}


# TODO: log the round trip on this server
@app.post("/deID", response_class=JSONResponse)
async def deID(req: Request):
    req_data = await req.json()
    _req = DeIDRequest.parse_obj(req_data)
    annotations = await spacy_c.deID(_req)
    res = DeIDResponse(data={"docs": annotations}, req_id=_req.req_id)
    return res


@app.put("/deID", response_class=JSONResponse)
async def deID(req: Request):
    # TODO: logic to utilize deidentification updates from the UI via a controller
    req_data = await req.json()
    _req = DeIDRequest.parse_obj(req_data)
    _res = await feedback_c.update_deID(_req)

    return _res
