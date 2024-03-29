from uuid import uuid4
from datetime import datetime
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")

from pydantic import BaseModel, ValidationError, validator, root_validator
from ._Token import _Token
from ._Entity import _Entity


class _Doc(BaseModel):
    name: str = "doc"
    # TODO: need to figure out how we're keeping track of these
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    text: str
    entities: List[_Entity]
    tokens: List[_Token]
