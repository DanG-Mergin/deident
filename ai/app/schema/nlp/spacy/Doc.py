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
    entities: List[SpacyEntityInstance]
    # tokens: List[Token]

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

        # TODO: need to associate entities and tokens.. use map_tokens
        # sents = values.pop("sents", None)
        # if sents:
        #     values["tokens"] = [Token(t) for t in sents.split(' ')]
        return values

    # def _map_tokens(doc: str, ents: list):
    #     tokens = []
    # for each entity get the start and end characters, find the tokens, add as ids to entities, add as tokens here
    # it might be better to pull tokens from the text value in entities, using the offset of start, end, etc
