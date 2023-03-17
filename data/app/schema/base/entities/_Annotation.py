from uuid import uuid4
from datetime import datetime
from dateutil.parser import isoparse
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Entity import _Entity


class _Annotation(BaseModel):
    model_name: str = "annotation"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    author_id: str
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow()))
    entities: List[_Entity]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values

    @validator("timestamp")
    def iso8601_date(cls, v):
        """
        Converts the timestamp string to an ISO 8601 formatted string.
        """
        dt = isoparse(v)
        return dt.isoformat()
