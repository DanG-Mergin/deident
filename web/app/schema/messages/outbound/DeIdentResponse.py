import os
import sys
from typing import Dict, List
from pydantic import ValidationError, validator, root_validator, Extra, Field

# TODO: fix all this stupid pathing
# sys.path.append("..schema")
from ._Observable import _Observable
from ...nlp.Doc import Doc

# from ._Response import _Response


class SocDeIdentResponse(_Observable, extra=Extra.ignore):
    data: Dict[str, List[Doc]]
    # req_id: UUID = Field(default_factory=uuid4)
    # orig_id: str = Field(alias="orig_id")
    # o_action: str = Field(alias="action")
    # o_status: str = Field(alias="status")
    # o_type: str = Field(alias="type")
    # entity: str = Field(alias="entity")

    # @property
    # def req_id(self):
    #     return self._req_id

    # @property
    # def orig_id(self):
    #     return self.orig_id

    # @property
    # def o_action(self):
    #     return self.o_action

    # @property
    # def o_status(self):
    #     return self.o_status

    # @property
    # def o_type(self):
    #     return self.o_type

    # @property
    # def entity(self):
    #     return self.entity

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     annotations = values.pop("annotations", None)
    #     if annotations:
    #         values["data"] = {"annotations": annotations}

    #     return values
