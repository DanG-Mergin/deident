from uuid import uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")

from pydantic import BaseModel, ValidationError, validator, root_validator
from ._Token import _Token
from ._Entity import _Entity


class _Doc(BaseModel):
    name: str = "doc"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    entities: Optional[List[_Entity]]
    tokens: Optional[List[_Token]]
