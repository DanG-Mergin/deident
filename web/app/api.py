from fastapi import FastAPI, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os, logging, sys, json

sys.path.append(".")
# from .schema.ai.DeIDRequest import DeIDRequest

from .schema.ui.Observable import UIObservableRequest, UIObservableResponse

# from .schema.base.messages._MessageEnums import MsgAction, MsgType, MsgStatus, MsgEntity
from .controllers import ai, dictionary, data
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
        f"http://{os.environ['AI_SERVICE_DOMAIN']}:{os.environ['AI_SERVICE_PORT']}",
        f"http://{os.environ['UI_SERVICE_DOMAIN']}:{os.environ['UI_SERVICE_PORT']}",
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
    return {"Hello": "Fromweb_api"}


# TODO: the api should use models to validate requests - define in webfirst
# @app.post("/deID/", response_class=JSONResponse)
# async def deID(req: Request):
#     _req = cast_to_class(
#         req,
#         DeIDRequest,
#         data={
#             "docs": [
#                 "The words “dog”, “cat” and “banana” are all pretty common in English, so they’re part of the pipeline’s vocabulary, and come with a vector. The word “afskfsd” on the other hand is a lot less common and out-of-vocabulary – so its vector representation consists of 300 dimensions of 0, which means it’s practically nonexistent. If your application will benefit from a large vocabulary with more vectors, you should consider using one of the larger pipeline packages or loading in a full vector package, for example, en_core_web_lg, which includes 685k unique vectors. spaCy is able to compare two objects, and make a prediction of how similar they are. Predicting similarity is useful for building recommendation systems or flagging duplicates. For example, you can suggest a user content that’s similar to what they’re currently looking at, or label a support ticket as a duplicate if it’s very similar to an already existing one. Each Doc, Span, Token and Lexeme comes with a .similarity method that lets you compare it with another object, and determine the similarity. Of course similarity is always subjective – whether two words, spans or documents are similar really depends on how you’re looking at it. spaCy’s similarity implementation usually assumes a pretty general-purpose definition of similarity."
#             ]
#         },
#     )
#     res = await ai.deID(_req)
#     return res


socket_mgr = SocketManager()

# TODO: display connection status in UI
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await socket_mgr.connect(websocket)
    try:
        while True:
            json_data = await websocket.receive_json()
            try:
                _req = UIObservableRequest.parse_obj(json_data)
            except json.JSONDecodeError:
                # Handle the JSONDecodeError exception
                pass
            # TODO: move this into a socket controller
            if _req.msg_action == "read":
                try:
                    res = await data.read(_req)
                    _res = cast_to_class(
                        _req,
                        UIObservableResponse,
                        data=res.data,
                        msg_status="success",
                    )
                    await websocket.send_json(_res.dict())
                except Exception as e:
                    print(str(e))

            elif _req.msg_action == "search":
                try:
                    res = await data.search(_req)
                    # TODO: handle specific search types
                    _res = cast_to_class(
                        _req,
                        UIObservableResponse,
                        data=res.data,
                        msg_status="success",
                    )
                    await websocket.send_json(_res.dict())
                except Exception as e:
                    print(str(e))
            elif _req.msg_entity == "annotation":
                if _req.msg_action == "create":
                    try:
                        res = await data.update_deID(_req)
                        _res = cast_to_class(
                            _req,
                            UIObservableResponse,
                            data=res.data,
                            msg_status="success",
                        )
                        await websocket.send_json(_res.dict())
                    except Exception as e:
                        print(str(e))
            elif _req.msg_entity == "doc":
                if _req.msg_action == "create":
                    try:
                        res = await data.create_doc(_req)
                        # res = await ai.deID(_req)
                        _res = cast_to_class(
                            _req,
                            UIObservableResponse,
                            data=res.data,
                            msg_status="success",
                        )
                        await websocket.send_json(_res.dict())
                    except Exception as e:
                        print(str(e))

    except WebSocketDisconnect:
        socket_mgr.disconnect(websocket)
