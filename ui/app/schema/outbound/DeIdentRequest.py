import os
import sys
from pydantic import ValidationError, validator, root_validator

sys.path.append("..")
from ._PostRequest import _PostRequest


class DeIdentRequest(_PostRequest):
    url = f"{os.environ['AI_DEIDENT_URL']}"

    @root_validator
    def convert_fields(cls, values):
        docs = values.pop("docs", None)
        if docs:
            values["data"] = {"docs": docs}

        return values
