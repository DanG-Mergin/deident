from uuid import uuid4
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity
from ..messages._MessageEnums import Msg_Action, Msg_Entity


class _Change(BaseModel):
    name: str = "change"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    action: str
    entity: str
    timestamp: datetime = datetime.utcnow()
    # TODO: for now only handles _Entity, but should be able to handle any
    object: _Entity

    @validator("action")
    def map_action(cls, v):
        if v is None:
            return None
        return Msg_Action[v.lower()].value

    @validator("entity")
    def map_entity(cls, v):
        if v is None:
            return None
        return Msg_Entity[v.lower()].value
