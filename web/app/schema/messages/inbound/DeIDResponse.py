from typing import Dict, List
from pydantic import ValidationError, validator, root_validator

from ._Observable import _Observable
from ._Response import _Response
from ...nlp.Doc import Doc


class DeIDResponse(_Response):
    data: Dict[str, List[Doc]]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        # id = values.pop("id", None)
        # if id and id is not None:
        #     values["doc_id"] = id
        return values
