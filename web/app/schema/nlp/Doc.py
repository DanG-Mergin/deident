from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")

from pydantic import ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance
from .Vocab import VocabItem


class Doc(VocabItem):
    # TODO: need to figure out how we're keeping track of these
    doc_id: Optional[str] = Field(default_factory=uuid4, alias="id")
    text: str
    entities: List[EntityInstance]
    tokens: List[Token]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     id = values.pop("id", None)
    #     if id and id is not None:
    #         values["doc_id"] = id
    #     return values
