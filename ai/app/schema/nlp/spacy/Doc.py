# Taken from https://github.com/explosion/projects/blob/v3/tutorials/rel_component/assets/annotations.jsonl

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, ValidationError, validator, root_validator

import sys

sys.path.append("..")
from .Entity import SpacyEntityInstance
from .Token import Token


class Doc(BaseModel):
    id = "fake_id_fix_me"
    text: str
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
