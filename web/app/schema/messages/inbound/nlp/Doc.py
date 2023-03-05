from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
from ....nlp.Token import Token
from ....nlp.Entity import EntityInstance

# TODO: rework inheritance this is a mess
class Doc(BaseModel):
    uuid: Optional[str] = Field(default_factory=uuid4)
    text: str
    entities: Optional[List[EntityInstance]] = []
    tokens: Optional[List[Token]] = []

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _entities = values.pop("_entities", None)
        if _entities:
            values["entities"] = _entities

        _tokens = values.pop("_tokens", None)
        if _tokens:
            values["tokens"] = _tokens
        # id = values.pop("id", None)
        # if id and id is not None:
        #     values["uuid"] = id
        return values
