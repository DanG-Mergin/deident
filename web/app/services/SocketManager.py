from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from ..schema.ui import Observable as Observable
from ..schema.base.messages._MessageEnums import (
    O_Action,
    O_Status,
    O_Type,
    UI_Entity,
    UI_EntityType,
    Job_Task,
    ElasticMethod,
    ElasticIndexes,
    ElasticTasks,
)

# https://medium.com/@pranata.giya12.gp/develop-a-chat-application-using-react-js-fastapi-and-websocket-5660143c4f80


class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    # TODO: This is where we will handle the incoming messages using a dispatch map to controllers
    # async def handle_request(self, obs: Observable):
