from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator


class _Entity(BaseModel):
    model_name: str = "entity"
    uuid: str
    label_id: Optional[str]
    start_index: int
    end_index: int
    start_char: Optional[int]
    end_char: Optional[int]
    text: Optional[str]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _endIndex = values.pop("_endIndex", None)
        if _endIndex:
            values["end_index"] = _endIndex

        _startIndex = values.pop("_startIndex", None)
        if _startIndex:
            values["start_index"] = _startIndex

        startIndex = values.pop("startIndex", None)
        if startIndex:
            values["start_index"] = startIndex

        startChar = values.pop("startChar", None)
        if startChar:
            values["start_char"] = startChar

        endChar = values.pop("endChar", None)
        if endChar:
            values["end_char"] = endChar

        labelId = values.pop("labelId", None)
        if labelId:
            values["label_id"] = labelId

        return values
