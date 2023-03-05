from typing import List, Dict
from pydantic import Extra, ValidationError, validator, root_validator

from ._Request import _Request
from .Doc import Doc


class DeIDRequest(_Request, extra=Extra.ignore):
    method: str = "POST"
    entity = "doc"
    data: Dict[str, List[Doc]]

    @property
    def docs(self):
        return (item for sublist in self.data.values() for item in sublist)
