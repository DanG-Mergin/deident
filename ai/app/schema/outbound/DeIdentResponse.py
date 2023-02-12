import os
import sys

sys.path.append("..")
from ._Response import _Response
from ..nlp.Doc import Doc
from typing import Any, Dict, Optional, List
from pydantic import ValidationError, validator, root_validator


class DeIdentResponse(_Response):
    data: Dict[str, List[Doc]]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
