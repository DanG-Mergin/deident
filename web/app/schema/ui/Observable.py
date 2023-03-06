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
from ..base.messages._Observable import _Observable


class Observable(_Observable, extra=Extra.ignore):
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

    def dict(self, *args, **kwargs):
        json_out = super().dict(*args, **kwargs)
        json_out["action"] = self.o_action
        json_out["status"] = self.o_status
        json_out["type"] = self.o_type

        json_out.pop("o_action", None)
        json_out.pop("o_status", None)
        json_out.pop("o_type", None)

        return json_out
