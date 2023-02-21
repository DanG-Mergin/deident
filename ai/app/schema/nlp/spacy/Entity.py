from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator
from uuid import uuid4


class EntityLabel(BaseModel):
    # TODO: we need an actual knowledge base with user defined and supplied descriptions
    kb_id: Optional[str]
    text: str


class SpacyEntityInstance(BaseModel, extra=Extra.ignore):
    # TODO: this may require a lookup but should have a single source
    id: str
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    start: int
    end: int
    start_char: int
    end_char: int
    label: EntityLabel
    model_type: str = "spacy"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        label_txt = values.pop("label_", None)
        if label_txt:
            values["label"] = EntityLabel(kb_id=values["kb_id"], text=label_txt)

        return values
