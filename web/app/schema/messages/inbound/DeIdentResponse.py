import os
import sys
from typing import Dict, List
from pydantic import ValidationError, validator, root_validator

sys.path.append("..schema")
from ._Observable import _Observable
from ._Response import _Response
from ...nlp.Doc import Doc

# class SocDeIdentResponse(_Observable):
#     # TODO: setup annotation entity
#     @root_validator(pre=True)
#     def convert_fields(cls, values):
#         annotations = values.pop("annotations", None)
#         if annotations:
#             values["data"] = {"annotations": annotations}

#         return values


class DeIdentResponse(_Response):
    data: Dict[str, List[Doc]]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
