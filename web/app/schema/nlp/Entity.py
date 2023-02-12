from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator
import sys

sys.path.append("..")
from .Vocab import VocabItem

# from .Span import Span
from .Token import Token


class EntityLabel(BaseModel):
    extra = "forbid"
    kb_id: str  # points to a description of the entity
    text: str
    # description: str


class EntityInstance(VocabItem):
    id: str
    # TODO: should be a list of label ids
    label: EntityLabel  # TODO: this should just be IDs
    token_ids: List[int]  # TODO: this should just be IDs
    text: str

    # @validator("token_ids", pre=True)
    # def set_token_ids(cls, v):
    #     if not isinstance(v, list):
    #         return [id for id in range(v["start"], v["end"])]
    #     return v
