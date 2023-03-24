import os, json, spacy
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
    MsgStatus,
)

# from ..schema.base.entities._Annotation import _Annotation
from ..schema.nlp.spacy.Corpus import NER_Corpus


# first we need to determine if a corpus needs to be updated
# 1. a document is created, updated, or deleted
# if created: the user enters meta data which is tied to corpus types
# the data server should update corpora based on the meta data, or use views
# to check against rules
# we first need rules for when a model should be trained

# base_path = "../../../private/i2b2"

# TODO: inject the pipeline
# https://spacy.io/usage/processing-pipelines
nlp = spacy.load("en_core_sci_sm")


async def gather_external_data() -> NER_Corpus:
    async def get_i2b2_data():
        _req = _Request(
            # msg_entity_type = MsgEntity_Type.deid,
            # msg_entity=MsgEntity.corpus,
            msg_action=MsgAction.read,
            msg_status=MsgStatus.pending,
            method="GET",
            endpoint="i2b2",
        )
        _res = await request.make_request(_req, res_cls=_Response, timeout=30)
        # print(_res)
        _res.data.items = [NER_Corpus(**c) for c in _res.data.items]
        return _res

    i2b2 = await get_i2b2_data()

    return i2b2.data.items[0]


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
    # _internal_docs = [NER_Corpus(**d) for d in _docs_res.data.items]
    _external_corpus = await gather_external_data()
    _external_corpus.add_docs(_docs_res.data.items)
    # print(_docs_res.data.items)
    return _external_corpus


# TODO: should be able to get spacy docbins and add to them
# async def get_spacy_file():

# TODO: this should probably be a service
# TODO: this should likely consume a config object
async def train_model():
    # 1 get the corpus
    _corpus = await gather_corpus(
        ["discharge_notes", "discharge_summary", "admission_notes"], ["ner", "deid"]
    )
    # 2 convert to spacy training format
    corpus_docs = _corpus.to_training_data()
    # [("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),]

    db = spacy.tokens.DocBin()
    for doc, annotations in corpus_docs:
        d_nlp = nlp(doc.text)
        ents = []
        for start, end, label in annotations:
            span = d_nlp.char_span(start, end, label=label)
            ents.append(span)
        d_nlp.ents = ents
        db.add(d_nlp)

    return db


async def should_train_model():
    # 1 get num relevant changes since last training
    # 2 compare against threshold
    pass
