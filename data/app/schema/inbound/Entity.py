from typing import Dict, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator


class Entity(BaseModel, extra=Extra.ignore):
    id: str
    uuid: str
    label_id: str
    start_index: int
    end_index: int
