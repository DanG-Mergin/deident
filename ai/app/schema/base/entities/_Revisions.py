from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ._Change import _Change

# TODO: not currently in use on ai server, and may not need to be
class _Revisions(BaseModel):
    name: str = "revisions"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    doc_id: str
    changes: List[_Change]
    timestamp: str = Field(default_factory=lambda: str(datetime.utcnow()))
    author_id: str
