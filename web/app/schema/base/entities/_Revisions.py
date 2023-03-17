from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Change import _Change


class _Revisions(BaseModel):
    model_name: str = "revisions"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    changes: List[_Change]
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow()))
    author_id: str

    @validator("changes", pre=True)
    def _convert_changes(cls, v):
        if v is None:
            return None
        return [_Change(**c) for c in v]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        if "docID" in values:
            values["doc_id"] = values.pop("docID")
        if "authorID" in values:
            values["author_id"] = values.pop("authorID")

        return values
