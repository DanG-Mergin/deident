import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import os
import sys

sys.path.append(".")
from .schema.inbound.DeIdentRequest import DeIdentRequest
from .schema.InternalMsg import InternalMsg
from .controllers import spacy as spacy_c

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


@app.post("/deident", response_class=JSONResponse)
async def deident(request: Request):
    b = request.json()
    res = await spacy_c.deident({"hi": "hihi"})
    return res


# @app.post("/deident/{DeIdentRequest}", response_class=JSONResponse)
# async def deident(req):
#     res = await spacy_c.deident(req)
#     return res


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8083, log_level="info")
