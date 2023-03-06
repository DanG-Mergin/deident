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
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    o_action: str
    o_status: str
    o_type: str
    task: Optional[str]
    entity: str
    entityType: str
    # data: Optional[_Data]
    data: Union[_Data, Dict[str, Any], None, Dict]

    # @property
    # def uuid(self):
    #     return str(self.uuid)

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
