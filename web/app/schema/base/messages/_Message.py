from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, Union
from pydantic import (
    BaseModel,
    Extra,
    Field,
    validator,
    root_validator,
    ValidationError,
    json,
)
from ._Data import _Data
from ._MessageEnums import (
    Msg_Status,
    Msg_Action,
    Msg_Type,
    Msg_Entity,
    Msg_Entity_Type,
    Msg_Task,
)


class _Message(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    msg_action: str
    msg_status: str
    msg_type: Optional[str]
    msg_task: Optional[str]
    msg_entity: Optional[str]
    msg_entity_type: Optional[str]
    data: Union[_Data, Dict[str, Any], None, Dict]

    @validator("msg_action")
    def map_action(cls, v):
        if v is None:
            return None
        return Msg_Action[v.lower()].value

    @validator("msg_status")
    def map_status(cls, v):
        if v is None:
            return None
        return Msg_Status[v.lower()].value

    @validator("msg_type")
    def map_type(cls, v):
        if v is None:
            return None
        return Msg_Type[v.lower()].value

    @validator("msg_task")
    def map_task(cls, v):
        if v is None:
            return None
        return Msg_Task[v.lower()].value

    @validator("msg_entity")
    def map_entity(cls, v):
        if v is None:
            return None
        return Msg_Entity[v.lower()].value

    @validator("msg_entity_type")
    def map_entityType(cls, v):
        if v is None:
            return None
        return Msg_Entity_Type[v.lower()].value

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values

    # exclude unset fields from the serialized output
    def to_json(self) -> str:
        return json.dumps(self.dict(exclude_unset=True))
