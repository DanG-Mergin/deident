from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class _Label(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    kb_id: str
    description: str
    text: str
    types: List[str]
    tasks: List[str]
    substitutionId: UUID
    category: str
    subCategory: str
    tag: str
    short_description: str
    instructions: str
    badgeName: str
    icon: str
