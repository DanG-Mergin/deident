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


async def get_external_docs() -> NER_Corpus:
    async def get_i2b2_data():
        _req_params = {
            # msg_entity_type = MsgEntity_Type.deid,
            # msg_entity=MsgEntity.corpus,
            "msg_action": MsgAction.read,
            "msg_status": MsgStatus.pending,
            "method": "GET",
        }
        train_req = _Request(
            **_req_params,
            endpoint="i2b2/train",
        )
        test_req = _Request(
            **_req_params,
            endpoint="i2b2/test",
        )
        train_res = await request.make_request(train_req, res_cls=_Response, timeout=60)
        test_res = await request.make_request(test_req, res_cls=_Response, timeout=60)

        # return [NER_Corpus(**c) for c in _res.data.items]
        _res = {
            "train": [NER_Corpus(**c) for c in train_res.data.items],
            "test": [NER_Corpus(**c) for c in test_res.data.items],
        }
        return _res

    i2b2 = await get_i2b2_data()

    return i2b2


async def get_internal_corpus(doc_types: List[str], tasks: List[str]) -> NER_Corpus:
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
        msg_entity=MsgEntity.corpus,
        msg_entity_type=MsgEntity_Type.deid,
        msg_action=MsgAction.search,
        query=_doc_query,
    )
    _docs_res = await request.make_request(_docs_req, res_cls=_Response, timeout=60)
    return NER_Corpus(**_docs_res.data.items[0])


# TODO: this should be a service?
async def get_corpus(doc_types: List[str], tasks: List[str]):
    _corpus = await get_internal_corpus(doc_types, tasks)

    # _corpus = await get_external_docs()

    # TODO: train test split should likely be happening here by proportion with new docs added to both train and test
    # add the new internal docs to the training corpus
    # _corpus["train"][0].add_docs(_internal_corpus[0]["docs"])

    return _corpus


async def _to_doc_bin(_corpus: NER_Corpus):
    corpus_docs = (
        _corpus.to_training_data()
    )  # [("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),]
    db = spacy.tokens.DocBin()
    for text, entities in corpus_docs:
        try:
            l = len(text)
            d_nlp = nlp(text)
            ents = []
            for start, end, tag in entities:
                s = text[start:end]
                print(s)
                span = d_nlp.char_span(start, end, label=tag)
                ents.append(span)
            d_nlp.ents = ents
            db.add(d_nlp)
        except Exception as e:
            print(e)

    return db


# import spacy
# from spacy.tokens import DocBin
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
from spacy.scorer import Scorer


def evaluate(nlp, test_data):
    scorer = Scorer(nlp)
    for example in test_data:
        predicted = nlp(example.text)
        scorer.score(predicted, example.reference)
    return scorer.scores


# TODO: should be able to get spacy docbins and add to them
# TODO: need to track which IDs have been added to the docbin
# async def get_spacy_file():

# TODO: this should probably be a service
# TODO: this should likely consume a config object
async def train_ner():
    # 1 get the corpus
    _corpus = await get_corpus(
        ["discharge_notes", "discharge_summary", "admission_notes"], ["ner"]
    )

    # 2 convert to spacy training format
    # train_data = await _to_doc_bin(_corpus["train"][0])
    # test_data = await _to_doc_bin(_corpus["test"][0])
    doc_bin = await _to_doc_bin(_corpus)

    train_data = []
    test_data = []

    for doc in doc_bin.get_docs(nlp.vocab):
        example = Example.from_dict(doc, doc.to_dict())
        if random.random() < 0.8:  # 80% training data, 20% evaluation data
            train_data.append(example)
        else:
            test_data.append(example)

    # 3 train the model

    # model = "en_core_web_sm"
    # nlp = spacy.load(model) if model else spacy.blank("en")
    n_iter = 30  # Number of training iterations

    # Disable other components for faster training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*other_pipes):
        # Initialize optimizer
        # if we aren't using a pre-built model:
        # if not model:
        #     nlp.begin_training()
        optimizer = nlp.resume_training()

        # Training loop
        for i in range(n_iter):
            random.shuffle(train_data)
            losses = {}

            # Batch training data
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.5, sgd=optimizer, losses=losses)

            print(f"Losses at iteration {i}: {losses}")

    ner_scores = evaluate(nlp, test_data)
    print(ner_scores)


async def should_train_model():
    # 1 get num relevant changes since last training
    # 2 compare against threshold
    pass
