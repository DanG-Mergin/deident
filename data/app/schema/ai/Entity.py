from uuid import uuid4
from datetime import datetime
from dateutil.parser import isoparse
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

from ..base.entities._Entity import _Entity
from ...services import label as label_svc


class NER_Entity(BaseModel, extra=Extra.ignore):
    start_char: int
    end_char: int
    tag: str

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _category = values.get("category", None)
        _tag = values.get("tag", None)

        if _category and _tag is None:
            values["tag"] = _category

        return values

    @staticmethod
    async def convert_from_base(e: _Entity):
        label = await label_svc.get_label_by_id(e.label_id)
        tag = label.tag
        ner_ent = {
            "uuid": e.uuid,
            "start_char": e.start_char,
            "end_char": e.end_char,
            "tag": tag,
        }
        return NER_Entity(**ner_ent)
