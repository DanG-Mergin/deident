import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._Response import _Response


class DeIDResponse(_Response):
    # This is from the webserver

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
