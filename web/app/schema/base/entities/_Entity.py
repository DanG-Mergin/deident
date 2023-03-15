from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator


class _Entity(BaseModel):
    name: str = "entity"
    id: str
    uuid: str
    label_id: Optional[str]
    start_index: int
    end_index: int
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

        labelId = values.pop("labelId", None)
        if labelId:
            values["label_id"] = labelId

        return values
