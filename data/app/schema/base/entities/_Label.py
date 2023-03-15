from typing import List, Optional, Union
from uuid import uuid4
from pydantic import BaseModel, root_validator, validator
from ..messages._MessageEnums import Msg_Task


class _Label(BaseModel):
    name: str = "label"
    uuid: str
    description: str
    types: List[str]
    tasks: List[str]
    category: str
    subCategory: str
    tag: str
    short_description: str
    instructions: str
    kb_id: Union[str, None] = None
    substitutionId: Union[str, None] = None
    badgeName: Union[str, None] = None
    icon: Union[str, None] = None

    @validator("tasks")
    def map_task(cls, tasks):
        return [Msg_Task[t.lower()].value for t in tasks]
