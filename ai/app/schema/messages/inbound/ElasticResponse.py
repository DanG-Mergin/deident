from typing import Dict, List
from pydantic import ValidationError, validator, root_validator
from ._Response import _Response
from ...nlp.Doc import Doc


class ElasticResponse(_Response):
    data: Dict[str, List[Dict]]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        # id = values.pop("id", None)
        # if id and id is not None:
        #     values["uuid"] = id
        return values