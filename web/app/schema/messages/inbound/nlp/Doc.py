from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")


class Doc(BaseModel):
    doc_id: Optional[str] = Field(default_factory=uuid4, alias="id")
    text: str
    annotations: Optional[Dict[str, Any]]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     id = values.pop("id", None)
    #     if id and id is not None:
    #         values["doc_id"] = id
    #     return values
