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


# first we need to determine if a corpus needs to be updated
# 1. a document is created, updated, or deleted
# if created: the user enters meta data which is tied to corpus types
# the data server should update corpora based on the meta data, or use views
# to check against rules
# we first need rules for when a model should be trained


async def gather_external_data():
    async def get_i2b2_data():
        pass


# TODO: this should be a service?
async def gather_corpus(doc_types: List[str], tasks: List[str]):
    _doc_query = {
        "query": {
            "bool": {
                "must": [
                    {"terms": {"doc_types": doc_types}},
                    # {"terms": {"tasks": ["ner", "deid"]}},
                ]
            }
        }
    }
    # 1. get all documents that match the doc_types and tasks
    _docs_req = _ElasticRequest(
        msg_entity=MsgEntity.doc,
        msg_entity_type=MsgEntity_Type.ner,
        msg_action=MsgAction.search,
        query=_doc_query,
    )
    _docs_res = await request.make_request(_docs_req, res_cls=_Response)

    print(_docs_res.data.items)
    return _docs_res


# TODO: this should probably be a service
# TODO: this should likely consume a config object
async def train_model():
    # 1 get the corpus
    _res = await gather_corpus(
        ["discharge notes", "discharge summary", "admission notes"], ["ner", "deid"]
    )
    return _res


async def should_train_model():
    # 1 get num relevant changes since last training
    # 2 compare against threshold
    pass
