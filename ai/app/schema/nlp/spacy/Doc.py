# Adapted from https://github.com/explosion/projects/blob/v3/tutorials/rel_component/assets/annotations.jsonl

from __future__ import annotations
from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

# import spacy
# from spacy.tokens import DocBin
from ....schema.base.entities._Doc import _Doc
from ....schema.base.entities._Entity import _Entity
from ....schema.base.entities._Token import _Token
from .Entity import SpacyEntityInstance, NER_Entity
from .Token import Token


class NER_Doc(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    name = "ner_doc"
    text: str  # the text of the document
    entities: List[NER_Entity]
    tokens: List[_Token]

    def __init__(self, **kwargs):
        _ents = []
        if kwargs["tokens"] is not None and len(kwargs["tokens"]) > 0:
            _ents = self._map_tokens_to_ents(kwargs["tokens"], kwargs["ents"])
        else:
            raise ValueError("tokens must be a list of Token objects")

        if kwargs["labels"] is not None and len(kwargs["labels"]) > 0:
            _ents = self._map_labels_to_ents(kwargs["labels"], kwargs["ents"])
        else:
            raise ValueError("labels must be a list of Label objects")

        kwargs["entities"] = [NER_Entity(e) for e in _ents]

        super().__init__(**kwargs)

    def _map_tokens_to_ents(self, tokens: List[_Token], ents: List[_Entity]):
        _ents = []
        _sorted_tokens = sorted(tokens, key=lambda t: t.start_char)

        for e in ents:
            new_e = {
                "start_char": None,
                "end_char": None,
                "tag": None,
                "label_id": e.label_id,
            }
            for t in _sorted_tokens:
                if e.start_index == t.index:
                    new_e["start_char"] = t["start_char"]
                if e.end_index == t.index:
                    new_e["end_char"] = t["end_char"]
                    break
                elif e.end_index > t.index:
                    break
            _ents.append(new_e)

        return _ents

    def _map_labels_to_ents(self, labels: List[Dict], ents: List[Dict]):
        for e in ents:
            if e["tag"] is None:
                for l in labels:
                    if l["uuid"] == e["label_id"]:
                        # NOTE: ignoring subcategories for now
                        e["tag"] = l["category"]
                        break

        return ents

    def to_training_data(self):
        return (self.text, [e.to_training_data() for e in self.entities])

    # def to_doc_bin(self):
    #     nlp = spacy.blank("en")
    #     db = DocBin()
    #     training_data = (self.doc, self.ents)
    #     for text, annotations in training_data:
    #         doc = nlp(text)
    #         ents = []
    #         for start, end, label in annotations:
    #             span = doc.char_span(start, end, label=label)
    #             ents.append(span)
    #         doc.ents = ents
    #         db.add(doc)
    # return DocBin().from_bytes(self.json().encode("utf8"))


class Doc(_Doc, extra=Extra.ignore):
    entities: List[SpacyEntityInstance]
    tokens: List[Token]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        ents = values.pop("ents", None)
        if ents:
            values["entities"] = [
                SpacyEntityInstance(
                    label_=e.label_,
                    id=e.id,
                    kb_id=e.kb_id,
                    text=e.text,
                    start=e.start,
                    end=e.end,
                    start_char=e.start_char,
                    end_char=e.end_char,
                )
                for e in ents
            ]
        tokens = values.pop("tokens", None)
        if tokens:
            values["tokens"] = [
                Token(
                    text=t.text,
                    id=t.i,
                    index=t.i,
                    lemma=t.lemma,
                    lemma_=t.lemma_,
                    whitespace_=t.whitespace_,
                    start_char=t.idx,
                    end_char=t.idx + len(t.text),
                )
                for t in tokens
            ]
            # values["tokens"] = cls._map_tokens(cls, values["entities"])
        return values

    # These methods are not used, but I'm keeping them here for now
    # they work but I'm handling this in the UI for now as entities are meant to change
    # which tokens they are associated with

    # def _split_entity(e: SpacyEntityInstance):
    #     tokens = []
    #     words = e.text.split(" ")
    #     start_char = e.start_char
    #     id = e.start
    #     for w in words:
    #         # if w.isalnum():
    #         end_char = start_char + len(w)
    #         tokens.append(
    #             Token(text=w, start_char=start_char, end_char=end_char, id=id)
    #         )
    #         start_char = end_char + 1
    #         id = id + 1
    #     return tokens

    # def _map_tokens(cls, ents: list):
    #     tokens = []
    #     for e in ents:
    #         if e.end - e.start == 1:
    #             # there is only one token in this entity
    #             tokens.append(
    #                 Token(
    #                     text=e.text,
    #                     start_char=e.start_char,
    #                     end_char=e.end_char,
    #                     id=e.start,
    #                 )
    #             )
    #         else:
    #             # There are multiple tokens in this entity
    #             tokens = tokens + cls._split_entity(e)
    #     return tokens
