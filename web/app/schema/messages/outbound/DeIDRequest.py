import os
import sys
from pydantic import ValidationError, validator, root_validator, Extra
from typing import List, Dict

# TODO: do I only need to append .. once?
from ._Request import _Request
from ..inbound.nlp.Doc import Doc


class DeIDRequest(_Request, extra=Extra.ignore):
    method = "POST"
    url = f"{os.environ['AI_DEIDENT_URL']}"
    data: Dict[str, List[Doc]]
