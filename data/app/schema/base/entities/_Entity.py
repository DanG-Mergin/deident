from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator


class _Entity(BaseModel):
    id: str
    uuid: str
    label_id: Optional[str]
    start_index: int
    end_index: int
