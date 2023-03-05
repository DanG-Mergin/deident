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
from .._MessageEnums import (
    O_Status,
    O_Action,
    O_Type,
    UI_Entity,
    UI_EntityType,
    Job_Task,
)


class _Observable(BaseModel, extra=Extra.allow):
    req_id: str = Field(default_factory=lambda: str(uuid4()))
    orig_id: str
    o_action: str
    o_status: str
    o_type: str
    task: Optional[str]
    entity: str
    entityType: str
    data: Optional[dict]

    @validator("o_action")
    def map_action(cls, value):
        return O_Action[value.lower()].value

    @validator("o_status")
    def map_status(cls, value):
        return O_Status[value.lower()].value

    @validator("o_type")
    def map_type(cls, value):
        return O_Type[value.lower()].value

    @validator("task")
    def map_task(cls, value):
        if value is None:
            return None
        return Job_Task[value.lower()].value

    @validator("entity")
    def map_entity(cls, value):
        return UI_Entity[value.lower()].value

    @validator("entityType")
    def map_entityType(cls, value):
        return UI_EntityType[value.lower()].value

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
