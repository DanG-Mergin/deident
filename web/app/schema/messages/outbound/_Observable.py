from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import (
    BaseModel,
    Extra,
    Field,
    validator,
    root_validator,
    ValidationError,
    json,
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
    ElasticMethod,
    ElasticIndexes,
    ElasticTasks,
)


class _Observable(BaseModel, extra=Extra.ignore):
    # the alias is used to map the field name to the name used during serialzation
    _req_id: str = Field(default_factory=lambda: str(uuid4()))
    orig_id: str
    o_action: str
    o_status: str
    o_type: str
    task: Optional[str]
    entity: str
    entityType: str
    data: Optional[dict]

    @property
    def req_id(self):
        return str(self._req_id)

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
        return values

    # exclude unset fields from the serialized output
    def to_json(self) -> str:
        return json.dumps(self.dict(exclude_unset=True))
