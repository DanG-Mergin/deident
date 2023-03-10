from pyee import EventEmitter
from fastapi_websocket_pubsub import PubSubClient
import asyncio
from .schema.base.messages._MessageEnums import Msg_Entity, Msg_Action, Msg_Task
from .schema.base.messages._Observable import _Observable

ee = EventEmitter()

# @ee.on('event')


class _Emitter:
    _instance = None

    # singleton instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribe()
        return cls._instance

    def _broadcast(cls, message):
        # ee.emit("doc_create", message)
        ee.emit(message.msg_entity, message)
        ee.emit(f"{message.msg_entity}_{message.msg_action}", message)
        ee.emit(f"{message.msg_entity}_{message.msg_task}", message)
        ee.emit(
            f"{message.msg_entity}_{message.msg_action}_{message.msg_task}", message
        )
        return message

    async def _handle_socket_event(cls, data, topic):
        print(data)
        print(topic)
        _message = _Observable(**data)
        cls._broadcast(_message)
        return _message

    def _subscribe(cls):
        client = PubSubClient(keep_alive=True)
        client.start_client("ws://data-service:8082/pubsub")
        client.subscribe("all", cls._handle_socket_event)


emitter = _Emitter()
