import os
import sys
from typing import Dict, List
from pydantic import ValidationError, validator, root_validator, Extra

# TODO: fix all this stupid pathing
# sys.path.append("..schema")
from ._Observable import _Observable
from ...nlp.Doc import Doc

# from ._Response import _Response


class SocDeIdentResponse(_Observable, extra=Extra.ignore):
    data: Dict[str, List[Doc]]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
