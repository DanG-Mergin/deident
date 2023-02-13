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
    # time_start: datetime = Field(default_factory=datetime.utcnow)
    # time_end: Optional[datetime]
    data: Optional[dict]

    # def __init__(cls, **data):
    #     super().__init__(**data)
    #     cls.data = data.get("data", None)
    #     class.status
    # @validator("o_status")
    # def check_status(cls, v):
    #     if v not in O_Status:
    #         raise ValueError("invalid status")
    #     return O_Status[v]

    # @validator("o_action")
    # def check_action(cls, v):
    #     if v not in O_Action:
    #         raise ValueError("invalid action")
    #     return O_Action[v]

    # @validator("o_type")
    # def check_type(cls, v):
    #     if v not in O_Type:
    #         raise ValueError("invalid type")
    #     return O_Type[v]

    # @validator("entity")
    # def check_entity(cls, v):
    #     if v not in UI_Entity:
    #         raise ValueError("invalid entity")
    #     return UI_Entity[v]

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

        # entity = values.pop("entity", None)
        # if entity and entity is not None:
        #     values["entity"] = entity

        # orig_id = values.pop("orig_id", None)
        # if orig_id and orig_id is not None:
        #     values["orig_id"] = orig_id

        return values
