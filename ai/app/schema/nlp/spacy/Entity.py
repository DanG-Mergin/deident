from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

# from uuid import uuid4
from ...base.entities._Entity import _Entity


class EntityLabel(BaseModel):
    # TODO: we need an actual knowledge base with user defined and supplied descriptions
    kb_id: Optional[str]
    text: str


class SpacyEntityInstance(_Entity):
    start_char: int
    end_char: int
    label: EntityLabel
    model_type: str = "spacy"

    class Config:
        fields = {
            "start_index": "start",
            "end_index": "end",
        }

    @root_validator(pre=True)
    def convert_fields(cls, values):
        label_txt = values.pop("label_", None)
        if label_txt:
            values["label"] = EntityLabel(kb_id=values["kb_id"], text=label_txt)

        return values
