import os
import sys

sys.path.append("..")
from ._Response import _Response
from ..nlp.Doc import Doc
from typing import Any, Dict, Optional, List
from pydantic import ValidationError, validator, root_validator


class DeIdentResponse(_Response):
    # annotations: List[Doc]
    # data: Optional[Dict]
    # url = f"{os.environ['AI_DEIDENT_URL']}"
    # docs: List[str]

    # @validator("docs")
    # def enforce_is_list(cls, v):
    #     if not isinstance(v, list):*
    #         return [v]
    #     return v

    # TODO: consider moving this to the base request class
    # take the "data" field from requests and set properties on this class
    @root_validator(pre=True)
    def convert_fields(cls, values):
        annotations = values.pop("annotations", None)
        if annotations:
            values["data"] = {"annotations": annotations}

        return values
