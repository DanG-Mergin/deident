from typing import Dict, List
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field
from ..base.messages._Observable import _Observable
from .Doc import Doc
from ..base.messages._Data import _Data

# from ._Response import _Response


class Data(_Data):
    items: List[Doc]


class SocDeIDResponse(_Observable):
    # data: Dict[str, List[Doc]]
    # TODO: ensure that all requests have entities as appropriate
    entity = "doc"
    data: Data

    # TODO: clean this up
    @root_validator(pre=True)
    def convert_fields(cls, values):
        # # values.pop("entity", None)
        # # docs = values.get("docs")
        # data = values.pop("data", None)
        # if data:
        #     # if all checks pass, return the original values
        #     values["data"] = {"docs": data}
        return values
