import os, json, spacy
from pathlib import Path
from typing import List, Generator
from ..emitter import ee

from ..services.spacy import spacy as spacy_s
from ..services.utils import cast_to_class
from ..services import request
from ..services import label as label_svc

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
# nlp = spacy.load("en_core_sci_sm")

nlp = spacy.blank("en")


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


async def _add_labels_to_model(model):
    # TODO: this should be model and component specific
    # TODO: we're currently only using the "category" label
    labels = await label_svc.get_categories()
    ner_comp = model.get_pipe("ner")
    ner_labels_in_model = list(ner_comp.labels)
    labels_to_add = [l for l in labels if l not in ner_labels_in_model]
    for l in labels_to_add:
        ner_comp.add_label(l)

    print(ner_labels_in_model)


async def _to_doc_bin(corpus: NER_Corpus, prev_doc_bin=spacy.tokens.DocBin()):
    await _add_labels_to_model(nlp)
    ner_comp = nlp.get_pipe("ner")
    print(list(ner_comp.labels))

    corpus_docs = (
        corpus.to_training_data()
    )  # [("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),]

    doc_bin = prev_doc_bin
    accepted_count = 0
    rejected_ents = []
    for text, entities in corpus_docs:
        ents = []
        l = len(text)
        d_nlp = nlp(text)

        for start, end, tag in entities:
            try:
                # print(s)
                span = d_nlp.char_span(start, end, label=tag)
                # span = d_nlp.char_span(start, end, label=tag, alignment_mode="contract")
                # span = d_nlp.char_span(start, end, label=tag, alignment_mode="expand")
                # contract: In contract mode, the character span is contracted to the smallest span that completely covers all the tokens that intersect with it. This means that the start and end indices of the span are moved to the nearest token boundaries to include all the tokens that overlap with the span. This ensures that the output span is entirely contained within the tokens.
                # expand: In expand mode, the character span is expanded to include all tokens that intersect with it, even if only partially. This means that the start and end indices of the span are moved to the nearest token boundaries that intersect with the span. This ensures that the output span includes all the tokens that are even partially covered by the span.
                # ents.append(span)
                if span is None:
                    s = text[start:end]
                    rejected_ents.append((s, start, end, tag))
                else:
                    ents.append(span)
                    accepted_count = accepted_count + 1
            except Exception as e:
                print(e)
        d_nlp.ents = ents
        doc_bin.add(d_nlp)

    print(f"accepted: {accepted_count}")
    print(f"rejected: {len(rejected_ents)}")
    print("rejected ents: \n```````````````````````````` \n\n ")
    for s, start, end, tag in rejected_ents:
        print(s, start, end, tag)
    return doc_bin


# TODO: this is a crap hack
def _get_data_path():
    current_dir = Path(__file__).resolve().parent

    # Move up the directory tree to the ".ai" directory
    data_dir = current_dir.parents[1]
    return os.path.join(data_dir, "app", "assets", "data")


# TODO: needs to account for the specific model in use
# TODO: needs to use the data server
async def get_doc_bin(filename: str = "deid_corpus", attrs: List[str] = None):
    data_dir = _get_data_path()
    path = os.path.join(data_dir, f"{filename}.spacy")

    if os.path.exists(path):
        return spacy.tokens.DocBin().from_disk(path)
    elif attrs:
        return spacy.tokens.DocBin(attrs=attrs)

    return spacy.tokens.DocBin()


# TODO: needs to account for the specific model in use
# TODO: needs to use the data server
def save_doc_bin(doc_bin, filename: str = "deid_corpus"):
    try:
        data_dir = _get_data_path()
        path = os.path.join(data_dir, f"{filename}.spacy")
        doc_bin.to_disk(path)

    except Exception as e:
        print(f"error saving doc_bin to file {e}")


# import spacy
# from spacy.tokens import DocBin
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
from spacy.scorer import Scorer
from spacy.tokens import Span


def _split_data(data: list, split=0.8, seed=None):
    if seed is None:
        seed = int(os.environ.get("RANDOM_SEED"))

    random.seed(seed)
    random.shuffle(data)

    divider = int(len(data) * split)
    return data[:divider], data[divider:]


def evaluate(nlp, test_data):
    scorer = Scorer(nlp)
    for example in test_data:
        predicted = nlp(example.text)
        scorer.score(predicted, example.reference)
    return scorer.scores


import string


def check_annotations(examples):
    whitespace_rejects = []
    punctuation_rejects = []
    for text, annotations in examples:
        for start, end, label in annotations["entities"]:
            entity_text = text[start:end]
            if (
                entity_text[0] in string.whitespace
                or entity_text[-1] in string.whitespace
            ):
                # print(f"Entity '{entity_text}' has leading or trailing whitespace.")
                whitespace_rejects.append((start, end, label))
            if (
                entity_text[0] in string.punctuation
                or entity_text[-1] in string.punctuation
            ):
                # print(f"Entity '{entity_text}' has leading or trailing punctuation.")
                punctuation_rejects.append((start, end, label))

    print(
        f"leading rejects: {len(whitespace_rejects)}, trailing rejects: {len(punctuation_rejects)}"
    )


def trim_annotations(examples):
    new_examples = []
    # TODO: this label check doesn't belong here:
    label_set = set()
    for text, annotations in examples:
        new_annotations = []
        for start, end, label in annotations["entities"]:
            label_set.add(label)
            entity_text = text[start:end]
            if (
                entity_text[0] in string.whitespace
                or entity_text[0] in string.punctuation
            ):
                start = start + 1
            if (
                entity_text[-1] in string.whitespace
                or entity_text[-1] in string.punctuation
            ):
                end = end - 1
            new_annotations.append((start, end, label))
        new_examples.append((text, {"entities": new_annotations}))

    print(f"adjusted total for whitespace and punctuation: {len(new_examples)}")
    print(f"label set: {label_set}")
    return new_examples


def filter_annotations(examples):
    filtered = []

    def _filter_doc(doc, annotations):
        rejected = []
        accepted = []

        for anno in annotations:
            try:
                start, end, label = anno
                span = doc.char_span(start, end, label=label)
                if span is None:
                    s = text[start:end]
                    rejected.append((s, start, end, label))
                else:
                    accepted.append(anno)
            except Exception as e:
                print(e)

        return accepted, rejected

    for text, annotations in examples:
        doc = nlp(text)
        accepted, rejected = _filter_doc(doc, annotations["entities"])
        filtered.append((text, {"entities": accepted}))

    return filtered


from spacy.tokens import DocBin


def convert(examples):
    nlp = spacy.blank("en")
    db = DocBin()
    for text, annot in examples:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                print(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db
    # db.to_disk(output_path)
    # save_doc_bin(db)


async def train_from_scratch():
    n_epochs = 3
    nlp = spacy.blank("en")
    # ner = nlp.create_pipe("ner")
    nlp.add_pipe("ner", last=True)
    # await _add_labels_to_model(nlp)

    corpus = await get_corpus(
        ["discharge_notes", "discharge_summary", "admission_notes"], ["ner"]
    )
    corpus_docs = corpus.to_training_data()

    train_data, test_data = _split_data(corpus_docs, split=0.8)

    train_data = trim_annotations(train_data)
    test_data = trim_annotations(test_data)
    check_annotations(train_data)
    check_annotations(test_data)

    train_data = filter_annotations(train_data)
    test_data = filter_annotations(test_data)

    train_db = convert(train_data)
    save_doc_bin(train_db, "de-id-train")

    test_db = convert(test_data)
    save_doc_bin(test_db, "de-id-test")

    # train_examples = [
    #     Example.from_dict(nlp(text), annotations) for text, annotations in train_data
    # ]
    # test_examples = [
    #     Example.from_dict(nlp(text), annotations) for text, annotations in test_data
    # ]

    # optimizer = nlp.begin_training()
    # for i in range(n_epochs):
    #     random.shuffle(train_examples)
    #     batches = minibatch(train_examples, size=compounding(4.0, 32.0, 1.001))
    #     losses = {}
    #     for batch in batches:
    #         texts, annotations = zip(*batch)
    #         nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)

    #     print(f"Losses at iteration {i}: {losses}")

    # # nlp.to_disk("/path/to/your/model")

    # ner_scores = evaluate(nlp, test_examples)
    # print(ner_scores)


# TODO: should be able to get spacy docbins and add to them
# TODO: need to track which IDs have been added to the docbin
# async def get_spacy_file():
async def train_ner():
    await _add_labels_to_model(nlp)

    ner_comp = nlp.get_pipe("ner")
    # ner_labels_in_model = list(ner_comp.labels)

    # print(ner_labels_in_model)

    corpus = await get_corpus(
        ["discharge_notes", "discharge_summary", "admission_notes"], ["ner"]
    )
    corpus_docs = corpus.to_training_data()

    train_data, test_data = _split_data(corpus_docs, split=0.8)

    train_data = trim_annotations(train_data)
    test_data = trim_annotations(test_data)
    check_annotations(train_data)
    check_annotations(test_data)

    train_data = filter_annotations(train_data)
    test_data = filter_annotations(test_data)

    # train_examples = []
    # test_examples = []

    # for text, annotations in train_data:
    #     ex = Example.from_dict(nlp(text), annotations)
    #     train_examples.append(ex)

    # for text, annotations in train_data:
    #     alignment = spacy.training.offsets_to_biluo_tags(
    #         nlp.make_doc(text), annotations["entities"]
    #     )
    # print(alignment)

    train_examples = [
        Example.from_dict(nlp(text), annotations) for text, annotations in train_data
    ]
    test_examples = [
        Example.from_dict(nlp(text), annotations) for text, annotations in test_data
    ]

    # 3 train the model

    # model = "en_core_web_sm"
    # nlp = spacy.load(model) if model else spacy.blank("en")

    n_iter = 30  # Number of training iterations
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    # await _add_labels_to_model(nlp)

    with nlp.disable_pipes(*other_pipes):
        # Initialize optimizer
        # if we aren't using a pre-built model:
        # - using begin_training will initialize the model with random weights instead of the previous model's weights
        # - with an older model there may be issues using newer versions of spacy to resume training.. presumably
        # because the weighting scheme has changed.  As such we should probably just retrain from scratch except when using
        # a custom model... again this is using optimizer = nlp.create_optimizer()
        # if not model:
        #     nlp.begin_training()
        # optimizer = nlp.resume_training()
        # optimizer = nlp.begin_training()

        optimizer = nlp.create_optimizer()

        # Training loop
        for i in range(n_iter):
            random.shuffle(train_examples)
            losses = {}

            # Batch training data
            batches = minibatch(train_examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.5, sgd=optimizer, losses=losses)

            print(f"Losses at iteration {i}: {losses}")

    ner_scores = evaluate(nlp, test_examples)
    print(ner_scores)


# TODO: this should probably be a service
# TODO: this should likely consume a config object
async def train_ner_orig():
    # nlp = spacy.load("en_core_sci_sm")
    await _add_labels_to_model(nlp)
    # 1 get the corpus
    # _corpus = await get_corpus(
    #     ["discharge_notes", "discharge_summary", "admission_notes"], ["ner"]
    # )

    # 2 convert to spacy training format

    # TODO: load the existing docbin and add to it
    # prev_doc_bin = await get_doc_bin(attrs=["ENT_TYPE"])

    # TODO: once i2b2 is working we should combine that with a new docbin
    # doc_bin = await _to_doc_bin(_corpus)
    # save_doc_bin(doc_bin)

    # TODO: load the existing docbin and add to it
    prev_doc_bin = await get_doc_bin(attrs=["ENT_IOB", "ENT_TYPE"])

    # convert generator to list
    docs = list(prev_doc_bin.get_docs(nlp.vocab))
    train_data, test_data = _split_data(docs)

    # train_examples = [Example.from_dict(doc, doc) for doc in train_data]
    test_examples = [Example.from_dict(doc, doc) for doc in test_data]
    train_examples = [
        Example.from_dict(nlp.make_doc(doc.text), doc) for doc in train_data
    ]

    # 3 train the model

    # model = "en_core_web_sm"
    # nlp = spacy.load(model) if model else spacy.blank("en")
    n_iter = 30  # Number of training iterations

    # Disable other components for faster training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    # await _add_labels_to_model(nlp)

    with nlp.disable_pipes(*other_pipes):
        # Initialize optimizer
        # if we aren't using a pre-built model:
        # - using begin_training will initialize the model with random weights instead of the previous model's weights
        # if not model:
        #     nlp.begin_training()
        # optimizer = nlp.resume_training()
        optimizer = nlp.begin_training()

        # Training loop
        for i in range(n_iter):
            random.shuffle(train_examples)
            losses = {}

            # Batch training data
            batches = minibatch(train_examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.5, sgd=optimizer, losses=losses)

            print(f"Losses at iteration {i}: {losses}")

    ner_scores = evaluate(nlp, test_examples)
    print(ner_scores)


async def should_train_model():
    # 1 get num relevant changes since last training
    # 2 compare against threshold
    pass
