from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity


class _Annotation(BaseModel):
    name: str = "annotation"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    author_id: str
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow()))
    entities: List[_Entity]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values
