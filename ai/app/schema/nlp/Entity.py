from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator
import sys

sys.path.append("..")
from .Vocab import VocabItem

# from .Span import Span
# from .Token import Token


class EntityLabel(BaseModel):
    Extra = "ignore"
    kb_id: str  # points to a description of the entity
    text: str


class EntityInstance(VocabItem):
    id: str
    # TODO: should be a list of label ids
    label_id: Optional[str]  # TODO: this should just be IDs
    token_ids: List[int]  # TODO: this should just be IDs
    text: str
    start_index: int  # TODO: fix casing and consistency
    end_index: int

    @validator("token_ids", pre=True)
    def set_token_ids(cls, v):
        if not isinstance(v, list):
            return [id for id in range(v["start"], v["end"])]
        return v
