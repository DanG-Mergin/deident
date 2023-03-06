from typing import List, Dict, Union
from pydantic import BaseModel, root_validator
from ..entities._Doc import _Doc
from ..entities._Label import _Label


class _Data(BaseModel):
    item_ids: List[str]
    # items: List[Dict] | List[_Doc] | List[_Label]
    items: List[Union[Dict, _Doc, _Label]]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _item_ids = values.get("item_ids", None)
        _items = values.get("items", None)
        if not _item_ids and _items:
            values["item_ids"] = [item.uuid for item in _items]
        # item_ids = values.pop("item_ids", None)
        # if item_ids:
        #     values["item_ids"] = item_ids
        # elif "items" in values:
        #     values["item_ids"] = [item["uuid"] for item in values["items"]]

        return values
