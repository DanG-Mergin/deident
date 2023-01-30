from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator

import sys

sys.path.append("..")
from .Token import Token


class EntityLabel(BaseModel):
    kb_id: Optional[str]
    text: str


class SpacyEntityInstance(BaseModel):
    id: str
    # kb_id: str
    text: str  #
    start: int  #
    end: int  #
    start_char: int
    end_char: int
    # entities: List[Type["Entity"]] = []
    label: EntityLabel
    # lemma: str # TODO: should be attached to token not entity
    text: str
    # tokens: List[Token] TODO: map tokens, see spacy.Doc.py

    # @validator("tokens")
    # def access_tokens(cls, v):
    #     if not isinstance(v, list):
    #         tokens =

    @root_validator(pre=True)
    def convert_fields(cls, values):
        label_txt = values.pop("label_", None)
        if label_txt:
            values["label"] = EntityLabel(kb_id=values["kb_id"], text=label_txt)

        # ents = values.pop("ents", None)
        # if ents:
        #     for field_name in cls.__fields__:
        #         if field_name in data:
        #             values[field_name] = data[field_name]

        return values
