import os
from typing import List
from ..emitter import ee

from ..services import spacy as spacy_s
from ..services.utils import cast_to_class
from ..services import request
from ..schema.base.messages._Observable import _Observable
from ..schema.base.messages._ElasticRequest import _ElasticRequest
from ..schema.base.messages._Request import _Request
from ..schema.base.messages._Response import _Response
from ..schema.base.entities._Doc import _Doc
from ..schema.base.messages._MessageEnums import (
    MsgEntity,
    MsgEntity_Type,
    MsgAction,
    MsgTask,
)
from ..schema.base.entities._Annotation import _Annotation


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
async def handle_doc_created(message: _Observable):
    print("handling doc create")

    print(message)
    doc_id = message.data.item_ids[0]
    # doc_id = message.data.get("item_ids", [])[0]

    annotated_doc = await annotate_document(doc_id)
    await save_annotations(annotated_doc[0])
    return annotated_doc


async def annotate_document(doc_id: str) -> _Response:
    _res = await get_document(doc_id)
    annotations = await spacy_s.deID(_res.data.items)

    # res = cast_to_class(req, _Response, data={"items": annotations})
    return annotations


async def get_document(docID: str) -> _Response:
    _res = None
    try:
        _req = _ElasticRequest(
            data={"item_ids": [docID]},
            msg_action="read",
            msg_entity="doc",
            msg_task="deID",
            msg_type="data",
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


async def save_tokens(annotated_doc, msg_task, msg_entity_type) -> _Response:
    try:
        _req = _ElasticRequest(
            data={
                "items": [annotated_doc],
            },
            msg_action="update",
            msg_entity="doc",
            msg_task=msg_task,
            msg_entity_type=msg_entity_type,
            msg_type="data",
        )
        _res = await request.make_request(_req, res_cls=_Response)
        return _res
    except Exception as e:
        print(str(e))
        return e


async def save_entities(doc_id, entities, msg_task, msg_entity_type) -> _Response:
    try:
        anno = _Annotation(
            doc_id=doc_id,
            entities=entities,
            author_id="spaCy",  # should be model/pipeline id
        )
        _req = _ElasticRequest(
            data={"items": [anno]},
            msg_action="create",
            msg_type="data",
            msg_entity="annotation",
            msg_task=msg_task,
            msg_entity_type=msg_entity_type,
        )
        _res = await request.make_request(_req, res_cls=_Response)
        return _res
    except Exception as e:
        print(str(e))
        return e


async def save_annotations(annotated_doc, msg_task="deID", msg_entity_type="deID"):
    try:
        _token_res = await save_tokens(annotated_doc, msg_task, msg_entity_type)
        _entities_res = await save_entities(
            annotated_doc.uuid, annotated_doc.entities, msg_task, msg_entity_type
        )
        return _token_res, _entities_res

    except Exception as e:
        print(str(e))
        return e
