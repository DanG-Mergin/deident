from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Extra, Field, Json, root_validator


class _Response(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    # orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
    error: Optional[Dict]  # for sharing additional error data

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     _data = values.pop("data", None)
    #     if _data and _data is not None:
    #         values["data"] = _data
    #     return values
