from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from ..base.entities._Annotation import _Annotation

# from ..base.entities._Entity import _Entity
# from ..base.entities._Change import _Change


class Annotation(_Annotation):
    model_name = "ui_annotation"
    # entities: List[_Entity] = []

    @root_validator(pre=True)
    def _convert_fields(cls, values):
        values["name"] = "annotation"
        _changes = values.pop("changes", None)
        if _changes:
            values["entities"] = []
            for change in _changes[0:]:
                values["entities"].append(change.object)

        return values
