from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

# from uuid import uuid4
from ...base.entities._Entity import _Entity


class EntityLabel(BaseModel):
    # TODO: we need an actual knowledge base with user defined and supplied descriptions
    kb_id: Optional[str]
    tag: str


# TODO: should probably just rely on the data server to handle this ish
# For training spaCy
class NER_Entity(BaseModel, extra=Extra.ignore):
    model_name = "ner_entity"
    start_char: int
    end_char: int
    tag: str

    def to_training_data(self):
        return (self.start_char, self.end_char, self.tag)

    @root_validator(pre=True)
    def convert_fields(cls, values):
        # _label_id = values.get("label_id", None)
        _category = values.get("category", None)
        _tag = values.get("tag", None)

        if _category and _tag is None:
            values["tag"] = _category

        _start = values.pop("start", None)
        if _start is not None:
            values["start_char"] = int(values["start"])

        _end = values.pop("end", None)
        if _end is not None:
            values["end_char"] = int(values["end"])

        return values


class SpacyEntityInstance(_Entity):
    # start_char: int
    # end_char: int
    # label: EntityLabel
    # label_id: str
    model_type: str = "spacy"
    # category: str
    label_: str
    label_id: Optional[str]

    class Config:
        fields = {
            "start_index": "start",
            "end_index": "end",
            "extra": Extra.ignore,
        }

    @root_validator(pre=True)
    def convert_fields(cls, values):
        # label_txt = values.pop("label_", None)
        # if label_txt:
        #     # values["label"] = EntityLabel(kb_id=values["kb_id"], tag=label_txt)
        #     values["tag"] = label_txt
        # values["label_id"] = label_svc.get_label_by_props(label_txt)

        return values
