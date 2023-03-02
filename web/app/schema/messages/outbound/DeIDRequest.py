import os
import sys
from pydantic import ValidationError, validator, root_validator, Extra
from typing import List, Dict

# TODO: do I only need to append .. once?
from ._Request import _Request
from ..inbound.nlp.Doc import Doc


class DeIDRequest(_Request, extra=Extra.ignore):
    url = f"{os.environ['AI_DEIDENT_URL']}"
    data: Dict[str, List[Doc]]
    method = "POST"

    # @property
    # def url(this):
    #     query = this.query
    #     if this.item_ids is not None:
    #         # TODO: currently only handles one id
    #         return f"{os.environ['DATA_URL']}/elastic/{this.index}/{this.item_ids[0]}"
    #     if query is not None:
    #         return f"{os.environ['DATA_URL']}/elastic/{this.index}/{query}"
    #     return f"{os.environ['DATA_URL']}/elastic/{this.index}"

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _action = values.pop("o_action", None)
        if _action is not None:
            values["method"] = cls._set_method(_action)
        return values

    def _set_method(action):
        if action == "udpate":
            return "PUT"
        return "POST"
