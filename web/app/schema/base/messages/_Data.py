from typing import List, Dict, Union
from pydantic import BaseModel, root_validator, validator
from ..entities._Doc import _Doc
from ..entities._Label import _Label
from ..entities._Entity import _Entity
from ..entities._Token import _Token
from ..entities._Change import _Change
from ..entities._Revisions import _Revisions
from ..entities._Annotation import _Annotation


class _Data(BaseModel):
    item_ids: List[str]
    items: List[
        Union[Dict, _Doc, _Label, _Entity, _Token, _Change, _Revisions, _Annotation]
    ] = None

    @validator("items", "item_ids", pre=True, always=True)
    def ensure_list(cls, value):
        if value and not isinstance(value, list):
            return [value]
        return value

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _item_ids = values.get("item_ids", None)
        _items = values.get("items", None)
        if not _item_ids and _items:
            values["item_ids"] = [item["uuid"] for item in _items]

        return values
