from uuid import uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
from datetime import datetime
from ._Token import _Token
from ._Entity import _Entity


class _Doc(BaseModel):
    name: str = "doc"
    # TODO: need to figure out how we're keeping track of these
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    text: str
    entities: Optional[List[_Entity]]
    tokens: Optional[List[_Token]]
