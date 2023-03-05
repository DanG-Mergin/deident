from typing import Dict, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator


class Entity(BaseModel, extra=Extra.ignore):
    id: str
    uuid: str
    label_id: str  # TODO: this should just be IDs
    start_index: int  # TODO: fix casing and consistency
    end_index: int
