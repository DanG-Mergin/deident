import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .controllers import spacy as spacy_c
from .services import sockets

from datetime import datetime
import json

# from ai.api import api as ai_api
# from frontend.api import api as ui_api
# from backend.api import api as data_api

app = FastAPI()
log = logging.getLogger(__name__)

origins = [
    "http://localhost:8082",
    "http://localhost:8083",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "From ui_api"}


# TODO: the api should use models to validate requests
@app.get("/deident/")
async def deident():
    synthetic_phi_test = "Patient Dan Goldberg called in from 617-123-8899 complaining of acute lack of synthetic data."
    res = await spacy_c.deident({"doc": synthetic_phi_test})
    return res


s_manager = sockets.SocketManager()

# TODO: define data_models for ws req/res
# TODO: move endpoint definition into sockets.py
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await s_manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            message = {"time": current_time, "clientId": client_id, "message": data}
            await s_manager.broadcast(json.dumps(message))

    except WebSocketDisconnect:
        s_manager.disconnect(websocket)
        message = {"time": current_time, "clientId": client_id, "message": "Offline"}
        await s_manager.broadcast(json.dumps(message))
