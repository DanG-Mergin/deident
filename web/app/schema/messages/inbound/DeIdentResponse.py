import os
import sys
from typing import Dict, List
from pydantic import ValidationError, validator, root_validator

sys.path.append("..schema")
from ._Observable import _Observable
from ._Response import _Response
from ...nlp.Doc import Doc


class DeIdentResponse(_Response):
    data: Dict[str, List[Doc]]
