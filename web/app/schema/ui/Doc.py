from pydantic import (
    Extra,
    root_validator,
)
from typing import List
from ..base.entities._Doc import _Doc
from .Token import Token
from .Entity import Entity


class Doc(_Doc, extra=Extra.ignore):
    entities: List[Entity]
    tokens: List[Token]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        if "text" not in values:
            raise ValueError("text is a required field")
        if not isinstance(values["text"], str):
            raise ValueError("text must be a string")
        if "entities" not in values:
            raise ValueError("entities is a required field")
        if not isinstance(values["entities"], list):
            raise ValueError("entities must be a list")
        if "tokens" not in values:
            raise ValueError("tokens is a required field")
        if not isinstance(values["tokens"], list):
            raise ValueError("tokens must be a list")

        # if "labels" in values:
        #     if not isinstance(values["labels"], list):
        #         raise ValueError("labels must be a list")

        return values
