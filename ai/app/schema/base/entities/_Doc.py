from uuid import uuid4
from typing import Any, Dict, Optional, Type, List, Union
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
from datetime import datetime
from ._Token import _Token
from ._Entity import _Entity
from ._EntityEnums import DocType, PatientClass


class _Doc(BaseModel):
    model_name: str = "doc"
    title: Optional[str]
    # TODO: need to figure out how we're keeping track of these
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    text: str
    entities: Optional[List[_Entity]]
    tokens: Optional[List[_Token]]
    doc_types: Optional[List[str]]
    patient_classes: Optional[List[str]]

    @validator("doc_types")
    def map_doc_types(cls, v):
        if v is None:
            return None
        return [DocType[t.lower()].value for t in v]

    @validator("patient_classes")
    def map_patient_classes(cls, v):
        if v is None:
            return None
        return [PatientClass[p.lower()].value for p in v]
