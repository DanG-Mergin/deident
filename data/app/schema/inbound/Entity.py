from typing import Dict, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator


class EntityLabel(BaseModel):
    extra = "ignore"
    kbId: str  # points to a description of the entity
    text: str
    # TODO: FIX ME
    type = "ner"
    task = "deID"
    description = "I'm a fake description set on the web server"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        kbId = values.pop("kb_id", None)
        if kbId:
            values["kbId"] = kbId

        return values


class EntityInstance(BaseModel, extra=Extra.ignore):
    id: str
    uuid: str
    labelId: Optional[str]  # TODO: this should just be IDs
    startIndex: int
    endIndex: int
    # tokenIds: List[int]  # TODO: this should just be IDs
    text: str

    @root_validator(pre=True)
    def convert_fields(cls, values):
        labelId = values.pop("label_id", None)
        if labelId:
            values["labelId"] = labelId
        # tokenIds = values.pop("token_ids", None)
        # if tokenIds:
        #     values["tokenIds"] = tokenIds
        startIndex = values.pop("start_index", None)
        if startIndex:
            values["startIndex"] = startIndex
        endIndex = values.pop("end_index", None)
        if endIndex:
            values["endIndex"] = endIndex

        if "id" not in values:
            raise ValueError("id is a required field")
        if not isinstance(values["id"], str):
            raise ValueError("id must be a string")
        if "startIndex" not in values:
            raise ValueError("startIndex is a required field")
        if not isinstance(values["startIndex"], int):
            raise ValueError("startIndex must be an integer")
        if "endIndex" not in values:
            raise ValueError("endIndex is a required field")
        if not isinstance(values["endIndex"], int):
            raise ValueError("endIndex must be an integer")
        # if "tokenIds" not in values:
        #     raise ValueError("tokenIds is a required field")
        # if not isinstance(values["tokenIds"], list):
        #     raise ValueError("tokenIds must be a list")
        # if not all(isinstance(token_id, int) for token_id in values["tokenIds"]):
        #     raise ValueError("tokenIds must be a list of integers")
        if "text" not in values:
            raise ValueError("text is a required field")
        if not isinstance(values["text"], str):
            raise ValueError("text must be a string")

        if "labelId" in values and values["labelId"] is not None:
            if not isinstance(values["labelId"], str):
                raise ValueError("labelId must be a string")

        return values
