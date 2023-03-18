from .utils import cast_to_class
import copy
from .elastic import request as request_svc
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
# _labels_by_id = None


async def get_labels():
    if not _labels:

        # _req = _ElasticRequest(
        #     msg_entity=MsgEntity.label,
        #     msg_entity_type=MsgEntity_Type.dictionary,
        #     msg_action=MsgAction.read,
        #     msg_task=MsgTask.deid,
        #     msg_type=MsgType.data,
        # )
        _res = await request_svc.get_index("label")

    # TODO: proper error handling
    return [r["_source"] for r in _res]
    # return _res["data"]["items"]


def get_label_map(labels):
    label_map = {}
    for label in labels:
        # category = label.get("category")
        category = label["category"].upper()
        # sub_category = label.get("subcategory")
        # uuid = label.get("uuid")

        if category not in label_map:
            label_map[category] = {}

        label_map[category][label["subcategory"].upper()] = label

    return label_map


# async def get_label_by_id(label_id):
#     if _labels_by_id is None:
#         for label in get_labels():
#             _labels_by_id = {label["uuid"]: label}

#     return _labels_by_id.get(label_id, None)


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
            label = label_map[category][subcategory]
        elif category in label_map:
            label = label_map[category][category]
        else:
            label = label_map["ENTITY"]["ENTITY"]

        span["label_id"] = label["uuid"]
        span["category"] = label["category"]
        span["subcategory"] = label["subcategory"]

    return _sp_arr
