# Adapted from https://github.com/explosion/projects/blob/v3/tutorials/rel_component/assets/annotations.jsonl

from __future__ import annotations
from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict, Union
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

# import spacy
# from spacy.tokens import DocBin
from ....schema.base.entities._Doc import _Doc
from ....schema.base.entities._Entity import _Entity
from ....schema.base.entities._Token import _Token
from .Entity import SpacyEntityInstance, NER_Entity
from .Token import Token
from ....services import label as label_svc

import asyncio


class NER_Doc(BaseModel, extra=Extra.ignore):
    model_name = "ner_doc"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    name = "ner_doc"
    text: str  # the text of the document
    entities: List[NER_Entity]
    tokens: Optional[List[_Token]]

    def __init__(self, **kwargs):
        if kwargs.get("entities", None):
            kwargs["entities"] = [NER_Entity(**e) for e in kwargs["entities"]]

        super().__init__(**kwargs)

    # TODO: if this is going to be used, it needs to be a static method because of pydantic
    # def _map_labels_to_ents(self, ents: List[Dict]):
    #     for e in ents:
    #         if e["tag"] is None:
    #             if e["label_id"]:
    #                 lbl = asyncio.run(label_svc.get_label_by_id(e["label_id"]))
    #                 e["tag"] = lbl["category"]

    #     return ents

    def to_training_data(self):
        return (self.text, {"entities": [e.to_training_data() for e in self.entities]})


class Doc(_Doc, extra=Extra.ignore):
    entities: List[SpacyEntityInstance]
    tokens: List[Token]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        ents = values.pop("ents", None)
        if ents:
            ents = [
                SpacyEntityInstance(
                    label_=e.label_,
                    # category=e.label_,
                    # id=e.id,
                    # kb_id=e.kb_id,
                    # text=e.text,
                    start=e.start,
                    end=e.end,
                    start_char=e.start_char,
                    end_char=e.end_char,
                )
                for e in ents
            ]
            values["entities"] = ents
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
        return values

    async def map_labels(self, ents: List[Dict]):
        for e in ents:
            _label_txt = e.label_
            if _label_txt is not None:
                lbl_id = await label_svc.get_label_id_by_props(category=_label_txt)
                e.label_id = lbl_id

        return ents
