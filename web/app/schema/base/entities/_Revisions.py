from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Change import _Change


class _Revisions(BaseModel):
    name: str = "revisions"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    changes: List[_Change]
    submitted: datetime
    author_id: str

    class Config:
        fields = {
            "doc_id": "docID",
            "author_id": "authorID",
        }
