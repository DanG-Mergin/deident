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
        return O_Action[value].value

    @validator("o_status")
    def map_status(cls, value):
        return O_Status[value].value

    @validator("o_type")
    def map_type(cls, value):
        return O_Type[value].value

    @validator("task")
    def map_task(cls, value):
        if value is None:
            return None
        return Job_Task[value].value

    @validator("entity")
    def map_entity(cls, value):
        return UI_Entity[value].value

    @validator("entityType")
    def map_entityType(cls, value):
        return UI_EntityType[value].value

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values
        # TODO: add combining data from responses and requests
        # @root_validator(pre=True)
        # def consume_elastic_response(cls, values):
        #     _data = values.pop("data", None)
        #     if _data and _data is not None:
        #         if "item_ids" in _data:
        #             values["item_ids"] = _data["item_ids"]

        #     _method = values.pop("method", None)
        #     if _method is not None:
        #         values["o_action"] = _method

        #     _index = values.pop("index", None)
        #     if _index and _index is not None:
        #         values["entity"] = _index

        #     _task = values.pop("task", None)
        #     if _task and _task is not None:
        #         values["task"] = _task

        #     _entity = values.pop("entity", None)
        #     if _entity and _entity is not None:
        #         values["entity"] = _entity

        return values

    # exclude unset fields from the serialized output
    def to_json(self) -> str:
        return json.dumps(self.dict(exclude_unset=True))
