import logging
from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, sys

sys.path.append(".")

from .controllers.elastic.router import elastic_router
from .services.utils import cast_to_class


app = FastAPI()
log = logging.getLogger(__name__)
# ---------------------------------------------------#
# DEV
# ---------------------------------------------------#
if os.environ["ENV"] == "DEV":
    origins = [
        f"http://{os.environ['AI_SERVICE_DOMAIN']}",
        f"http://{os.environ['AI_SERVICE_DOMAIN']}:{os.environ['WEB_SERVICE_PORT']}",
        f"http://{os.environ['WEB_SERVICE_DOMAIN']}",
        f"http://{os.environ['WEB_SERVICE_DOMAIN']}:{os.environ['WEB_SERVICE_PORT']}",
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


@app.on_event("startup")
async def init():
    log.info("Starting up data_api")
    app.mount("/elastic/", elastic_router)


@app.get("/")
def read_root():
    save_annotations("I'm an annotation")
    return {"Hello": "From data_api"}
