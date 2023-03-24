from .utils import cast_to_class
import copy
from . import request
from typing import List, Dict
from ..schema.base.messages._ElasticRequest import _ElasticRequest
from ..schema.base.messages._Response import _Response
from ..schema.base.messages._MessageEnums import (
    MsgEntity,
    MsgEntity_Type,
    MsgAction,
    MsgTask,
    MsgType,
)
from ..schema.base.entities._Label import _Label

_labels = None
_labels_by_id = None
_label_map = None


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

            _req = _ElasticRequest(
                msg_entity=MsgEntity.label,
                msg_entity_type=MsgEntity_Type.dictionary,
                msg_action=MsgAction.read,
                msg_task=MsgTask.deid,
                msg_type=MsgType.data,
            )
            _res = await request.make_request(_req, res_cls=_Response)
            if _res.data.items:
                self._labels = [_Label(**l) for l in _res.data.items]
        return self._labels

    async def get_label_map(self):
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

            self._label_map = label_map

        return self._label_map

    async def get_label_by_id(self, label_id):
        if not self._labels_by_id:
            for label in await self.get_labels():
                self._labels_by_id[label.uuid] = label

        return self._labels_by_id.get(label_id, None)


label_store = LabelStore()


async def get_label_by_id(label_id):
    return await label_store.get_label_by_id(label_id)


async def get_label_id_by_props(category, subcategory=None):
    label_map = await label_store.get_label_map()
    category = category.upper()
    if subcategory is None:
        subcategory = category
    else:
        subcategory = subcategory.upper()

    if category in label_map and subcategory in label_map[category]:
        return label_map[category][subcategory]
    elif category in label_map:
        return label_map[category][category]

    return label_map["ENTITY"]["ENTITY"]


# expects category and subcategory
async def set_labels_by_props(span_array: List[Dict]):
    _sp_arr = copy.deepcopy(span_array)

    for span in _sp_arr:
        span["label_id"] = get_label_id_by_props(span["category"], span["subcategory"])

    return _sp_arr
