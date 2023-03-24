from uuid import uuid4
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity
from ..messages._MessageEnums import MsgAction, MsgEntity


class _Change(BaseModel):
    model_name: str = "change"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    action: str
    entity: str
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    object: _Entity

    @validator("action")
    def map_action(cls, v):
        if v is None:
            return None
        return MsgAction[v.lower()].value

    @validator("entity")
    def map_entity(cls, v):
        if v is None:
            return None
        return MsgEntity[v.lower()].value
