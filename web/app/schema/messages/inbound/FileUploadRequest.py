import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._Request import _Request


class FileUploadRequest(_Request):
    type = "dictionary"  # TODO: store a reference to an actual class here
    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
