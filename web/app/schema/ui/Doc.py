from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import (
    BaseModel,
    Extra,
    Field,
    Json,
    ValidationError,
    validator,
    root_validator,
)
from pydantic import ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance, EntityLabel
from ..nlp.Vocab import VocabItem


class Doc(BaseModel, extra=Extra.ignore):
    # TODO: need to figure out how we're keeping track of these
    uuid: Optional[str] = Field(default_factory=uuid4)
    text: str
    entities: List[EntityInstance]
    tokens: List[Token]
    # labels: List[EntityLabel] = []

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
