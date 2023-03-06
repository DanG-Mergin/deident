from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Extra, validator, root_validator, Extra
from .ElasticEnums import ElasticTasks


class Label(BaseModel, extra=Extra.ignore):
    uuid: UUID
    kb_id: Optional[str] = None
    types: List[str]
    tasks: List[str]
    category: str
    subCategory: str
    tag: str
    short_description: str
    description: str
    instructions: str
    substitutionId: Optional[UUID] = None
    badgeName: Optional[str] = None
    icon: Optional[str] = None

    @validator("tasks")
    def map_task(cls, tasks):
        return [ElasticTasks[t.lower()].value for t in tasks]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _tasks = values.pop("tasks", None)
        if _tasks and _tasks is not None:
            values["tasks"] = _tasks
        return values
