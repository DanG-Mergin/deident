from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field
from uuid import uuid4
from .Vocab import VocabItem

# from .Span import Span
# from .Token import Token


class EntityLabel(BaseModel, extra=Extra.ignore):
    kb_id: str  # points to a description of the entity
    text: str


class EntityInstance(VocabItem):
    id: str
    uuid: str
    # TODO: should be a list of label ids
    label_id: Optional[str]  # TODO: this should just be IDs
    # token_ids: List[int]  # TODO: this should just be IDs
    text: str
    start_index: int  # TODO: fix casing and consistency
    end_index: int

    # @validator("token_ids", pre=True)
    # def set_token_ids(cls, v):
    #     if not isinstance(v, list):
    #         return [id for id in range(v["start"], v["end"])]
    #     return v

    # spacy end index is the token AFTER the last token in the entity
    # converting it here to be the last token in the entity
    @root_validator(pre=True)
    def convert_fields(cls, values):
        if "model_type" in values and values["model_type"] == "spacy":
            values.pop("model_type", None)
            if "end_index" in values:
                values["end_index"] -= 1
        return values

    # @validator("uuid", pre=True)
    # def set_uuid(cls, v):
    #     if not v:
    #         return str(uuid4())
    #     return v
