from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity


class _Annotation(BaseModel):
    name = "annotation"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    author_id: str
    timestamp: datetime = datetime.utcnow()
    entities: List[_Entity] = []
