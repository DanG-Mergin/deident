import os
import sys
from typing import List, Dict
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._PostRequest import _PostRequest
from .Doc import Doc


class DeIdentRequest(_PostRequest):
    extra = "ignore"
    data: Dict[str, List[Doc]]

    @property
    def docs(self):
        return (item for sublist in self.data.values() for item in sublist)

    # @validator("docs")
    # def enforce_is_list(cls, v):
    #     if not isinstance(v, list):
    #         return [v]
    #     return v

    # # TODO: consider moving this to the base request class
    # # take the "data" field from requests and set properties on this class
    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     data = values.pop("data", None)
    #     if data:
    #         for field_name in cls.__fields__:
    #             if field_name in data:
    #                 values[field_name] = data[field_name]
    #     # convert doc to docs
    #     doc = values.pop("doc", None)
    #     if doc:
    #         values["docs"] = doc
    #     return values
