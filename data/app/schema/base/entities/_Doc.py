from uuid import uuid4
from datetime import datetime
from dateutil.parser import isoparse
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")

from pydantic import BaseModel, ValidationError, validator, root_validator
from ._Token import _Token
from ._Entity import _Entity


class _Doc(BaseModel):
    name: str = "doc"
    # TODO: need to figure out how we're keeping track of these
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    text: str
    entities: List[_Entity]
    tokens: List[_Token]

    @property
    def label_ids(self):
        return list(
            set(label_id for entity in self.entities for label_id in entity.label_id)
        )

    @validator("created_at")
    def iso8601_date(cls, v):
        """
        Converts the created_at string to an ISO 8601 formatted string for elastic.
        """
        dt = isoparse(v)
        return dt.isoformat()

    # def dict(self, *args, **kwargs):
    #     json_out = super().dict(*args, **kwargs)
    #     # json_out["label_ids"] = self.label_ids
    #     json_out.pop("label_ids", None)
    #     return json_out
