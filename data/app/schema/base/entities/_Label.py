from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Extra, Field, validator, root_validator, Extra
from ..messages._MessageEnums import ElasticTasks


class _Label(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
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
