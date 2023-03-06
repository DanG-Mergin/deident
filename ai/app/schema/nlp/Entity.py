from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field
from uuid import uuid4
from ..base.entities._Entity import _Entity

# from .Span import Span
# from .Token import Token


class EntityLabel(BaseModel, extra=Extra.ignore):
    kb_id: str  # points to a description of the entity
    text: str


class EntityInstance(_Entity, extra=Extra.ignore):

    # spacy end index is the token AFTER the last token in the entity
    # converting it here to be the last token in the entity
    @root_validator(pre=True)
    def convert_fields(cls, values):
        if "model_type" in values and values["model_type"] == "spacy":
            values.pop("model_type", None)
            if "end_index" in values:
                values["end_index"] -= 1
        return values
