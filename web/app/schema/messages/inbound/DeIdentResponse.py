import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._Observable import _Observable
from ._Response import _Response

class SocDeIdentResponse(_Observable):
    # TODO: setup annotation entity
    @root_validator(pre=True)
    def convert_fields(cls, values):
        annotations = values.pop("annotations", None)
        if annotations:
            values["data"] = {"annotations": annotations}

        return values

class DeIdentResponse(_Response):
    @root_validator(pre=True)
    def convert_fields(cls, values):
        annotations = values.pop("annotations", None)
        if annotations:
            values["data"] = {"annotations": annotations}

        return values
