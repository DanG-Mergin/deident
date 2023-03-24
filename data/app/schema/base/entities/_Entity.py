from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator


class _Entity(BaseModel):
    model_name: str = "entity"
    uuid: str
    label_id: Optional[str]
    start_index: int
    end_index: int
    start_char: int
    end_char: int
