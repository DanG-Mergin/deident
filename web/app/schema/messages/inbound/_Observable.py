from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import (
    BaseModel,
    Extra,
    Field,
    Json,
    ValidationError,
    validator,
    root_validator,
)
import sys

sys.path.append("..")
from .._MessageEnums import O_Status, O_Action, O_Type, UI_Entity


class _Observable(BaseModel, extra=Extra.allow):
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: str
    o_action: str
    o_status: str
    o_type: str
    entity: str
    data: Optional[dict]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _status = values.pop("status", None)
        if _status and _status is not None:
            values["o_status"] = _status

        _action = values.pop("action", None)
        if _action is not None:
            values["o_action"] = _action

        _type = values.pop("type", None)
        if _type and _type is not None:
            values["o_type"] = _type

        return values
