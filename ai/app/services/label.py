from .utils import cast_to_class
import copy
import request
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


async def get_labels():
    if not _labels:

        _req = _ElasticRequest(
            msg_entity=MsgEntity.label,
            msg_entity_type=MsgEntity_Type.dictionary,
            msg_action=MsgAction.read,
            msg_task=MsgTask.deid,
            msg_type=MsgType.data,
        )
        _res = await request.make_request(_req, res_cls=_Response)
        if _res.data.items:
            _labels = [_Label(l) for l in _res.data.items]
    # TODO: proper error handling
    return _labels


def get_label_map(labels):
    label_map = {}
    for label in labels:
        # category = label.get("category")
        category = label.category.upper()
        # sub_category = label.get("subCategory")
        # uuid = label.get("uuid")

        if category not in label_map:
            label_map[category] = {}

        label_map[category][label.subCategory.upper()] = label.uuid

    return label_map


def get_label_by_id(label_id):
    if not _labels_by_id:
        for label in get_labels():
            _labels_by_id = {label.uuid: label}

    return _labels_by_id.get(label_id, None)


# expects category and subcategory
async def get_labels_by_props(span_array: List[Dict]):
    # get all labels from db
    labels = await get_labels()
    label_map = get_label_map(labels)

    _sp_arr = copy.deepcopy(span_array)

    for span in _sp_arr:
        category = span["category"].upper()
        subcategory = span["subcategory"].upper()
        if category in label_map and subcategory in label_map[category]:
            span["label_id"] = label_map[category][subcategory]
        elif category in label_map:
            span["label_id"] = label_map[category][category]
        else:
            span["label_id"] = label_map["ENTITY"]["ENTITY"]

    return _sp_arr
