from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Extra, ValidationError, validator, root_validator

# import sys

# sys.path.append("..")


class _Request(BaseModel, extra=Extra.allow):
    # service_name: str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[str]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]] #TODO: ensure this field is of some type of schema
    data: Optional[Dict]

    # TODO: add validators where appropriate
    # @root_validator
    # def convert_fields(cls, values):
    #     docs = values.pop("docs", None)
    #     if docs:
    #         values["data"] = {"docs": docs}

    #     return values
