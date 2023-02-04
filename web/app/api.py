import logging
from fastapi import FastAPI, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import sys

sys.path.append(".")
from .schema.messages.outbound.DeIdentRequest import DeIdentRequest
from .schema.messages.inbound.FileUploadRequest import FileUploadRequest
from .controllers import ai
from .services.utils import cast_to_class
from .services.SocketManager import SocketManager

app = FastAPI()
log = logging.getLogger(__name__)
# ---------------------------------------------------#
# DEV
# ---------------------------------------------------#
if os.environ["ENV"] == "DEV":
    origins = [
        f"http://{os.environ['AI_SERVICE_DOMAIN']}",
        f"http://{os.environ['AI_SERVICE_DOMAIN']}:{os.environ['WEB_SERVICE_PORT']}",
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
    return {"Hello": "Fromweb_api"}


# TODO: the api should use models to validate requests - define in webfirst
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
    res = await ai.deident(_req)
    return res


# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     # TODO take file.type and compare against schema
#     return {"file_fids": [file.fid for file in files]}

socket_mgr = SocketManager()

# TODO: display connection status in UI   
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
