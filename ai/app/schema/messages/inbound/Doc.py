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
from ...nlp.Entity import EntityInstance
from ...nlp.Token import Token


class Doc(BaseModel):
    uuid: Optional[str] = Field(default_factory=uuid4)
    text: str
    entities: Optional[List[EntityInstance]] = []
    tokens: Optional[List[Token]] = []


# class Doc(BaseModel, extra=Extra.ignore):
#     # TODO: need to figure out how we're keeping track of these
#     uuid: Optional[str] = Field(default_factory=uuid4)
#     text: str
#     entities: List[EntityInstance]
#     tokens: List[Token]
#     labels: List[EntityLabel] = []
