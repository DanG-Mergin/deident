from ._Response import _Response
from ...nlp.Doc import Doc
from typing import Any, Dict, Optional, List
from pydantic import Extra, ValidationError, validator, root_validator


class DeIDResponse(_Response):
    data: Dict[str, List[Doc]]
