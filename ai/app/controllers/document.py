import os
from typing import List

# from fastapi_websocket_pubsub import PubSubClient
# import asyncio
from ..emitter import ee

# from pyee import EventEmitter
from ..services import spacy as spacy_s
from ..services.utils import cast_to_class
from ..services import request
from ..schema.base.messages._Observable import _Observable
from ..schema.base.messages._ElasticRequest import _ElasticRequest
from ..schema.base.messages._Request import _Request
from ..schema.base.messages._Response import _Response
from ..schema.base.entities._Doc import _Doc
from ..schema.base.messages._MessageEnums import Msg_Entity, Msg_Action, Msg_Task

# ee = EventEmitter()

# takes a previously unannotated text, backs it up in the database, and returns the annotated text
async def deID(req: _Request) -> _Response:
    # First we need to save the unannotated text to the database
    _res = await save_document(req)

    if _res:
        # If the save was successful we can annotate the text
        annotations = await spacy_s.deID(req.data.items)

        res = cast_to_class(req, _Response, data={"items": annotations})
    return res


# For handling user feedback
@ee.on("doc_update")
def handle_doc_update(message: _Observable):
    print("handling doc update")
    print(message)


@ee.on("doc_create")
def handle_doc_created(message: _Observable):
    print("handling doc create")
    print(message)


async def update_deID(req: _Request) -> _Response:
    # currently just saving these changes outright... however
    # we may want to save them as changes to the original document
    # _res = await save_document(req)
    _res = await compare_annotations(req)

    return _res


async def compare_annotations(req: _Request):
    doc = req.data.items[0]
    _res = await get_document(req.data.item_ids[0])
    prev_doc = _Doc(_res.data.items[0])

    # compare the two documents for changes
    # for ent in doc.ents:
    #     for prev_ent in prev_doc.ents:
    #         if ent.label_ == prev_ent.label_:
    #             if ent.text != prev_ent.text:

    return _res


async def get_document(docID: str) -> _Response:
    _res = None
    try:
        _req = _ElasticRequest(
            data={"item_ids": [docID]},
            msg_action="read",
            msg_entity="doc",
            msg_task="deID",
        )

        _res = await request.make_request(_req, res_cls=_Response)

    except Exception as e:
        print(str(e))
        return e
        # TODO: robust error handling
    return _res


async def save_document(req: _Request) -> _Response:
    _res = None
    try:
        _req = _ElasticRequest(**req.dict())
        _res = await request.make_request(_req, res_cls=_Response)

    except Exception as e:
        print(str(e))
        return e
        # TODO: robust error handling
    return _res


# async def handle_doc_updated(data, topic):
#     print("doc updated")
#     print(data)
#     print(topic)
#     return data


# async def subscribe():
#     client = PubSubClient(keep_alive=True)
#     client.start_client("ws://data-service:8082/pubsub")
#     client.subscribe("steel", handle_doc_updated)
#     client.subscribe("doc", handle_doc_updated)
#     # await client.wait_until_done()
#     return client
