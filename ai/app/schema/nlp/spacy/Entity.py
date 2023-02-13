from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator

import sys

sys.path.append("..")
from .Token import Token


class EntityLabel(BaseModel):
    kb_id: Optional[str]
    text: str


class SpacyEntityInstance(BaseModel, extra=Extra.ignore):
    id: str
    text: str
    start: int
    end: int
    start_char: int
    end_char: int
    label: EntityLabel
    text: str

    @root_validator(pre=True)
    def convert_fields(cls, values):
        label_txt = values.pop("label_", None)
        if label_txt:
            values["label"] = EntityLabel(kb_id=values["kb_id"], text=label_txt)

        return values
