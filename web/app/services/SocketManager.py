from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

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
