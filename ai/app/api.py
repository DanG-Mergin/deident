import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import os
import sys

sys.path.append(".")
from .schema.inbound.DeIdentRequest import DeIdentRequest
from .schema.outbound.DeIdentResponse import DeIdentResponse

from .controllers import spacy as spacy_c
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
        f"http://{os.environ['UI_SERVICE_DOMAIN']}",
        f"http://{os.environ['UI_SERVICE_DOMAIN']}:{os.environ['UI_SERVICE_PORT']}",
        # "http://localhost:8081",
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
@app.post("/deident", response_class=JSONResponse)
async def deident(req: Request):
    req_data = await req.json()
    _req = DeIdentRequest(data=req_data["data"], req_id=req_data["req_id"])
    annotations = await spacy_c.deident(_req)
    # TODO add field mapping between request and response to response object
    res = DeIdentResponse(annotations=annotations, req_id=_req.req_id)
    return res
