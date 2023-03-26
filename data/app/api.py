import logging
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import Response, JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import os, sys

sys.path.append(".")

from .controllers.elastic.router import elastic_router, init as init_elastic
from .services import i2b2 as i2b2_svc

# from .services.utils import cast_to_class
from .emitter import pubsub_router, emitter
from .schema.base.messages._Observable import _Observable
from .schema.base.messages._Response import _Response

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
    app.include_router(pubsub_router)

    await init_elastic()


@app.get("/")
def read_root():
    # save_annotations("I'm an annotation")
    return {"Hello": "From data_api"}


@app.get("/i2b2/{subdirectory}")
async def i2b2(subdirectory: Optional[str] = None):
    if subdirectory is None:
        # return both train and test
        train = await i2b2_svc.get_i2b2("train")
        test = await i2b2_svc.get_i2b2("test")
        docs = train + test
    else:
        docs = await i2b2_svc.get_i2b2(subdirectory)

    res = _Response(
        msg_action="read",
        msg_status="success",
        data={"items": docs},
    )
    return res


# TODO: for testing only
@app.get("/trigger")
async def trigger_events():
    # asyncio.create_task(events())
    _test_msg = _Observable(
        msg_action="create",
        msg_status="success",
        msg_type="data",
        msg_task="deID",
        msg_entity="doc",
        msg_entity_type="deID",
        data={},
    )
    await emitter.publish(_test_msg)
