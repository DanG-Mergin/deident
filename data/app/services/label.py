from .utils import cast_to_class
import copy
from .elastic import request as request_svc
from typing import List, Dict

from ..schema.base.entities._Label import _Label


class LabelStore:
    _instance = None
    _labels = None
    _labels_by_id = None
    _label_map = None

    # singleton instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_labels(self):
        if not self._labels:
            _res = await request_svc.get_index("label")
            # TODO: proper error handling
            self._labels = [_Label(**r["_source"]) for r in _res]

        return self._labels
        # return _res["data"]["items"]

    async def get_label_map(self):
        # TODO: this is silly... I should be simply returning
        # - a list of subcategories as keys with ids as values
        if not self._label_map:
            label_map = {}
            for label in await self.get_labels():
                # category = label.get("category")
                category = label.category.upper()
                # sub_category = label.get("subcategory")
                # uuid = label.get("uuid")

                if category not in label_map:
                    label_map[category] = {}

                label_map[category][label.subcategory.upper()] = label.uuid

                # NOTE: this means at present you can't recover the original label.
                # this all maps back to a category at the moment
                if len(label.synonyms) > 0:
                    for syn in label.synonyms:
                        label_map[category][syn.upper()] = label.uuid

            self._label_map = label_map

        return self._label_map

    async def get_label_by_id(self, label_id):
        if not self._labels_by_id:
            _lab_by_id = {}
            for label in await self.get_labels():
                _lab_by_id[label.uuid] = label
            self._labels_by_id = _lab_by_id

        return self._labels_by_id.get(label_id, None)


label_store = LabelStore()


async def get_label_by_id(label_id):
    return await label_store.get_label_by_id(label_id)


# TODO: this is silly... I should be simply using
# - a list of subcategories as keys with ids as values
async def get_label_id_by_props(category, subcategory=None):
    label_map = await label_store.get_label_map()
    category = category.upper()
    if subcategory is None:
        subcategory = category
    else:
        subcategory = subcategory.upper()

    if category in label_map and subcategory in label_map[category]:
        return label_map[category][subcategory]

    for k, v in label_map.items():
        if subcategory in v:
            return v[subcategory]

    if category in label_map:
        # returns a generic label for the category like [Date][Date]
        return label_map[category][category]

    # else:
    #     for k, v in label_map.items():
    #         if subcategory in v:
    #             return v[subcategory]

    return label_map["ENTITY"]["ENTITY"]


# expects category and subcategory
async def set_labels_by_props(span_array: List[Dict]):
    _sp_arr = copy.deepcopy(span_array)

    for span in _sp_arr:
        span["label_id"] = await get_label_id_by_props(
            span["category"], span["subcategory"]
        )
        label = await get_label_by_id(span["label_id"])
        span["category"] = label.category
        span["subcategory"] = label.subcategory

    return _sp_arr
