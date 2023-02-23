from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Extra, validator, root_validator, Extra
from .ElasticEnums import ElasticTasks


class Label(BaseModel, extra=Extra.ignore):
    category: str
    subCategory: str
    types: List[str]
    tag: str
    tasks: List[str]
    kb_id: Optional[str] = None
    uuid: UUID
    short_description: str
    description: str
    instructions: str
    substitutionId: Optional[UUID] = None
    badgeName: Optional[str] = None

    @validator("tasks")
    def map_task(cls, tasks):
        return [ElasticTasks[t].value for t in tasks]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _tasks = values.pop("tasks", None)
        if _tasks and _tasks is not None:
            values["tasks"] = _tasks
        return values
