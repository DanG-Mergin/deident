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
