import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._Observable import _Observable

# socket request for deidentification
class SocDeIdentRequest(_Observable):
    # TODO: set up docs type
    @root_validator
    def convert_fields(cls, values):
        docs = values.pop("docs", None)
        if docs:
            values["data"] = {"docs": docs}

        return values
