from typing import Dict, List, Optional, Type
from pydantic import BaseModel, ValidationError, validator, root_validator
import sys

sys.path.append("..")
from .Vocab import VocabItem

# from .Span import Span
from .Token import Token


class EntityLabel(BaseModel):
    extra = "ignore"
    kb_id: str  # points to a description of the entity
    text: str
    # description: str
    # TODO: FIX ME
    type = "ner"
    task = "deID"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        kbId = values.pop("kbId", None)
        if kbId:
            values["kb_id"] = kbId

        return values


class EntityInstance(VocabItem):
    id: str
    uuid: str
    # TODO: should be a list of label ids
    label_id: Optional[str]
    start_index: int
    end_index: int
    text: str

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

    #     labelId = values.pop("label_id", None)
    #     if labelId:
    #         values["label_id"] = labelId
    #     tokenIds = values.pop("token_ids", None)
    #     if tokenIds:
    #         values["token_ids"] = tokenIds
    #     startIndex = values.pop("start_index", None)
    #     if startIndex:
    #         values["start_index"] = startIndex
    #     endIndex = values.pop("end_index", None)
    #     if endIndex:
    #         values["end_index"] = endIndex

    #     return values
