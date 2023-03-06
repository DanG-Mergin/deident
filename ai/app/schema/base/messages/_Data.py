from typing import List, Dict, Union
from pydantic import BaseModel, root_validator
from ..entities._Doc import _Doc
from ..entities._Label import _Label


class _Data(BaseModel):
    item_ids: List[str]
    items: List[Union[_Doc, _Label, Dict]]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _item_ids = values.get("item_ids", None)
        _items = values.get("items", None)
        if not _item_ids and _items:
            values["item_ids"] = [item.uuid for item in _items]

        return values