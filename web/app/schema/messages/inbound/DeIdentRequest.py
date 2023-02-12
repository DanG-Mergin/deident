import os
import sys
from typing import List, Dict
from uuid import UUID, uuid4
from pydantic import ValidationError, validator, root_validator, BaseModel, Field

sys.path.append("..")
from ._Observable import _Observable
from .nlp.Doc import Doc
from .._MessageEnums import O_Status, O_Action, O_Type, UI_Entity

# socket request for deidentification
class SocDeIdentRequest(_Observable):
    extra = "ignore"
    # req_id: UUID = Field(default_factory=uuid4)
    # _orig_id: str  # from the ui for example
    # _o_action: str
    # _o_status: str
    # _o_type: str
    # _entity: str
    # docs: List[Doc]
    data: Dict[str, List[Doc]]

    # @validator("data")
    # def check_data(cls, v):
    #     if v is None:
    #         raise ValueError("data is required")
    #     elif "docs" not in v:
    #         raise ValueError("docs is required")
    #     else:
    #         d = Doc(v["docs"][0])
    #         _v = {"docs": [Doc(d) for d in v["docs"]]}
    #         return _v
    #     return v

    # @root_validator
    # def convert_fields(cls, values):
    #     print(values)
    #     data = values.pop("data", None)
    #     if data:
    #         for field_name in cls.__fields__:
    #             if field_name in data:
    #                 values[field_name] = data[field_name]
    # docs = data.get("docs", None)
    # if docs:
    #     values["docs"] = [Doc(d) for d in docs]
    #     values["data"] = {"docs": [Doc(d) for d in docs]}

    # status = values.pop("status", None)
    # if status:
    #     values["_o_status"] = status

    # action = values.pop("action", None)
    # if action:
    #     values["_o_action"] = action
    # type = values.pop("type", None)
    # if type:
    #     values["_o_type"] = type

    # entity = values.pop("entity", None)
    # if entity:
    #     values["_entity"] = entity

    # orig_id = values.pop("orig_id", None)
    # if orig_id:
    #     values["_orig_id"] = orig_id
    # return values
