import os
import sys
from pydantic import ValidationError, validator, root_validator, Extra
from typing import List, Dict

# TODO: do I only need to append .. once?
from ._PostRequest import _PostRequest
from ..inbound.nlp.Doc import Doc


class DeIdentRequest(_PostRequest, extra=Extra.ignore):
    url = f"{os.environ['AI_DEIDENT_URL']}"
    data: Dict[str, List[Doc]]

    # @root_validator
    # def convert_fields(cls, values):
    #     docs = values.pop("docs", None)
    #     if docs:
    #         values["data"] = {"docs": docs}

    #     return values
