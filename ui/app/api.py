import logging
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

sys.path.append(".")
from .schema.outbound.DeIdentRequest import DeIdentRequest
from .schema.InternalMsg import InternalMsg
from .controllers import ai
from .services import sockets
from .services.utils import cast_to_class


from datetime import datetime
import json

# from ai.api import api as ai_api
# from frontend.api import api as ui_api
# from backend.api import api as data_api

app = FastAPI()
log = logging.getLogger(__name__)
# ---------------------------------------------------#
# DEV
# ---------------------------------------------------#
if os.environ["ENV"] == "DEV":
    origins = [
        f"http://{os.environ['AI_SERVICE_DOMAIN']}",
        f"http://{os.environ['AI_SERVICE_DOMAIN']}:{os.environ['UI_SERVICE_PORT']}",
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
    return {"Hello": "From ui_api"}


# TODO: the api should use models to validate requests - define in UI first
@app.post("/deidentify/", response_class=JSONResponse)
async def deident(req: Request):
    _req = cast_to_class(
        req,
        DeIdentRequest,
        data={
            "docs": [
                "The words “dog”, “cat” and “banana” are all pretty common in English, so they’re part of the pipeline’s vocabulary, and come with a vector. The word “afskfsd” on the other hand is a lot less common and out-of-vocabulary – so its vector representation consists of 300 dimensions of 0, which means it’s practically nonexistent. If your application will benefit from a large vocabulary with more vectors, you should consider using one of the larger pipeline packages or loading in a full vector package, for example, en_core_web_lg, which includes 685k unique vectors. spaCy is able to compare two objects, and make a prediction of how similar they are. Predicting similarity is useful for building recommendation systems or flagging duplicates. For example, you can suggest a user content that’s similar to what they’re currently looking at, or label a support ticket as a duplicate if it’s very similar to an already existing one. Each Doc, Span, Token and Lexeme comes with a .similarity method that lets you compare it with another object, and determine the similarity. Of course similarity is always subjective – whether two words, spans or documents are similar really depends on how you’re looking at it. spaCy’s similarity implementation usually assumes a pretty general-purpose definition of similarity."
            ]
        },
    )
    # _req = DeIdentRequest(request)
    # msg = InternalMsg(
    #     data={
    #         "doc": "Patient Dan Goldberg called in from 617-123-8899 complaining of acute lack of synthetic data."
    #     },
    #     meta_type="deident",
    # )
    res = await ai.deident(_req)
    return res


# s_manager = sockets.SocketManager()

# TODO: define data_models for ws req/res
# TODO: move endpoint definition into sockets.py
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await s_manager.connect(websocket)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # await manager.send_personal_message(f"You wrote: {data}", websocket)
#             message = {"time": current_time, "clientId": client_id, "message": data}
#             await s_manager.broadcast(json.dumps(message))

#     except WebSocketDisconnect:
#         s_manager.disconnect(websocket)
#         message = {"time": current_time, "clientId": client_id, "message": "Offline"}
#         await s_manager.broadcast(json.dumps(message))
