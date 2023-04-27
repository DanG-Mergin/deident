from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import os, sys, logging

sys.path.append(".")

from .schema.base.messages._Request import _Request
from .schema.base.messages._Response import _Response

# from .emitter import ee, emitter
from .controllers import document as document_c

from .controllers import train as train_c

# from .services.utils import cast_to_class

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
def read_root():
    return {"Hello": "From ml_app"}


@app.get("/testTraining")
async def test_training():
    # _res = await train_c.train_ner()
    # _res = await train_c.train_from_scratch()
    # return _res
    return {"message": "hello from testTraining"}


@app.get("/testMedTraining")
async def test_med_training():
    _res = await train_c.train_med_ner()
    return _res


# TODO: log the round trip on this server
# @app.post("/deID", response_class=JSONResponse)
# async def deID(req: Request):
#     req_data = await req.json()
#     _req = _Request.parse_obj(req_data)
#     res = await document_c.deID(_req)

#     return res


# no longer supported.  Handled with websockets
@app.put("/deID", response_class=JSONResponse)
async def deID(req: Request):
    # TODO: logic to utilize deidentification updates from the UI via a controller
    # req_data = await req.json()

    # _req = _Request.parse_obj(req_data)
    # _res = await document_c.update_deID(_req)

    # return _res
    return {"message": "no longer supported"}
