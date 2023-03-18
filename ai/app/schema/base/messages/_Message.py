from uuid import uuid4
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
    MsgStatus,
    MsgAction,
    MsgType,
    MsgEntity,
    MsgEntity_Type,
    MsgTask,
)


class _Message(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    msg_action: str
    msg_status: str = Field(default=MsgStatus.pending.value)
    msg_type: Optional[str]
    msg_task: Optional[str]
    msg_entity: Optional[str]
    msg_entity_type: Optional[str]
    query: Optional[Dict] = None
    data: Union[_Data, Dict[str, Any], None, Dict]

    @validator("msg_action")
    def map_action(cls, v):
        if v is None:
            return None
        return MsgAction[v.lower()].value

    @validator("msg_status")
    def map_status(cls, v):
        if v is None:
            return None
        return MsgStatus[v.lower()].value

    @validator("msg_type")
    def map_type(cls, v):
        if v is None:
            return None
        return MsgType[v.lower()].value

    @validator("msg_task")
    def map_task(cls, v):
        if v is None:
            return None
        return MsgTask[v.lower()].value

    @validator("msg_entity")
    def map_entity(cls, v):
        if v is None:
            return None
        return MsgEntity[v.lower()].value

    @validator("msg_entity_type")
    def map_entityType(cls, v):
        if v is None:
            return None
        return MsgEntity_Type[v.lower()].value

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values

    # exclude unset fields from the serialized output
    def to_json(self) -> str:
        return json.dumps(self.dict(exclude_unset=True))
