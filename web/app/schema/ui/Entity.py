from typing import Dict, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator
from ..base.entities._Entity import Entity as _Entity


class Entity(_Entity):
    labelId: Optional[str]  # TODO: this should just be IDs
    startIndex: int
    endIndex: int

    class Config:
        fields = {
            "extra": Extra.ignore,
            "labelId": "label_id",
            "startIndex": "start_index",
            "endIndex": "end_index",
        }
