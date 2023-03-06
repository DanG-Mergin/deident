import os
from pydantic import ValidationError, validator, root_validator, Extra
from typing import List, Dict

# TODO: do I only need to append .. once?
from ..base.messages._Request import _Request

# from ..messages.inbound.Doc import Doc
from ..base.entities._Doc import _Doc


class DeIDRequest(_Request, extra=Extra.ignore):
    url = f"{os.environ['AI_DEIDENT_URL']}"
    # data: Dict[str, List[_Doc]]
    method = "POST"
    entity = "doc"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _action = values.pop("o_action", None)
        if _action is not None:
            values["method"] = cls._set_method(_action)
        return values

    def _set_method(action):
        if action == "update":
            return "PUT"
        return "POST"
