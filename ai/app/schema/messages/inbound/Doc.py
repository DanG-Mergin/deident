from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")


class Doc(BaseModel):
    doc_id: Optional[str] = Field(default_factory=uuid4, alias="id")
    text: str
    annotations: Optional[Dict[str, Any]]
