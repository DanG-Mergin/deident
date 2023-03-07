from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, root_validator, validator
from ..messages._MessageEnums import Msg_Task


class _Label(BaseModel):
    uuid: str
    description: str
    types: List[str]
    tasks: List[str]
    category: str
    subCategory: str
    tag: str
    short_description: str
    instructions: str
    kb_id: Optional[str] = None
    substitutionId: Optional[UUID] = None
    badgeName: Optional[str] = None
    icon: Optional[str] = None

    @validator("tasks")
    def map_task(cls, tasks):
        return [Msg_Task[t.lower()].value for t in tasks]
