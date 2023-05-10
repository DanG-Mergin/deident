from typing import List, Optional, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


# TODO: this is really a UI Label, not a base Label
class _Label(BaseModel):
    model_name: str = "label"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    kb_id: Union[str, None] = None
    description: str
    text: str
    types: List[str]
    tasks: List[str]
    substitutionId: Union[str, None] = None
    category: str
    subcategory: str
    tag: str
    short_description: str
    instructions: str
    badgeName: str
    icon: str
