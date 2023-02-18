import os
import sys
from typing import Dict, List
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field

# TODO: fix all this stupid pathing
# sys.path.append("..schema")
from ._Observable import _Observable
from ...ui.Doc import Doc

# from ._Response import _Response


class SocDeIDResponse(_Observable):
    data: Dict[str, List[Doc]]
    entity = "doc"

    # TODO: clean this up
    @root_validator(pre=True)
    def convert_fields(cls, values):
        values.pop("entity", None)
        data = values.get("docs")
        if data:
            # if all checks pass, return the original values
            values["data"] = {"docs": data}
        return values
