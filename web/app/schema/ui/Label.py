from typing import List
from uuid import UUID
from pydantic import BaseModel


class Label(BaseModel):
    uuid: UUID
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
