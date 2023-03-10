import os
from pydantic import ValidationError, validator, root_validator, Extra
from typing import List, Dict

from ..base.messages._Request import _Request


class DeIDRequest(_Request, extra=Extra.ignore):
    _url = f"{os.environ['AI_DEIDENT_URL']}"
    msg_entity = "doc"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _action = values.get("msg_action", None)
        if _action is not None:
            values["method"] = cls._set_method(_action)
        return values

    def _set_method(action):
        if action == "update":
            return "PUT"
        return "POST"
