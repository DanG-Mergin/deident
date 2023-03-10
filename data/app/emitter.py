from fastapi import APIRouter, HTTPException, Request
from starlette.websockets import WebSocket
from fastapi_websocket_pubsub import PubSubEndpoint
import asyncio
from .schema.base.messages._Message import _Message

pubsub_router = APIRouter()


_endpoint = PubSubEndpoint()
_endpoint.register_route(pubsub_router)


class _Emitter:
    _instance = None

    # singleton instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def publish(cls, message: _Message):
        await _endpoint.publish(
            # can sub to specific entity or all events
            [message.msg_entity, "all"],
            message,
        )
        return message


# import this to publish messages
emitter = _Emitter()
