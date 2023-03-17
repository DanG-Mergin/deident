from uuid import uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
from datetime import datetime
from pydantic import BaseModel, ValidationError, validator, root_validator
from ._Token import _Token
from ._Entity import _Entity


class _Doc(BaseModel):
    model_name: str = "doc"
    title: Optional[str]
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    text: str
    entities: Optional[List[_Entity]]
    tokens: Optional[List[_Token]]
    doc_types: Optional[List[str]]
    patient_classes: Optional[List[str]]
