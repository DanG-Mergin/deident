from typing import List, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class _Label(BaseModel):
    name: str = "label"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    kb_id: Union[str, None] = None
    description: str
    types: List[str]
    tasks: List[str]
    substitutionId: Union[str, None] = None
    category: str
    subCategory: str
    tag: str
    short_description: str
    instructions: str
    badgeName: str
    icon: str
