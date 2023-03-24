from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity


class _Annotation(BaseModel):
    model_name: str = "annotation"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    author_id: str = "spaCy"
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    entities: List[_Entity]

    # @validator("entities", pre=True)
    # def cast_ents(cls, v):

    #     return [_Entity.parse_obj(e.dict()) for e in v]
