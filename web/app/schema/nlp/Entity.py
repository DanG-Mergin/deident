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
    task = "deident"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        kbId = values.pop("kbId", None)
        if kbId:
            values["kb_id"] = kbId

        return values


class EntityInstance(VocabItem):
    id: str
    # TODO: should be a list of label ids
    label_id: Optional[str]
    start_index: int
    end_index: int
    token_ids: List[int]
    text: str

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
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
