import os
import sys
from typing import List, Dict
from pydantic import Extra, ValidationError, validator, root_validator

sys.path.append("..")
from ._PostRequest import _PostRequest
from .Doc import Doc


class DeIDRequest(_PostRequest, extra=Extra.ignore):
    data: Dict[str, List[Doc]]

    @property
    def docs(self):
        return (item for sublist in self.data.values() for item in sublist)
