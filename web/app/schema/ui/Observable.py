from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import (
    BaseModel,
    Extra,
    Field,
    Json,
    ValidationError,
    validator,
    root_validator,
)
from ..base.messages._Observable import _Observable
from .Doc import Doc as UIDoc
from .Entity import Entity as Entity
from .Token import Token as Token
from ..base.entities._Change import _Change as Change
from ..base.entities._Revisions import _Revisions as Revisions
from ..base.entities._Label import _Label as Label

MODEL_MAP = {
    "revisions": Revisions,
    "doc": UIDoc,
    "entity": Entity,
    "token": Token,
    "change": Change,
    "label": Label,
}


class UIObservableRequest(_Observable):
    def __init__(self, **kwargs):
        # handle docs and revisions
        kwargs["data"] = self._cast_data(kwargs["data"])
        super().__init__(**kwargs)

    def _cast_data(self, data):
        _items = data.items
        if _items and isinstance(_items, list):
            _data = {"item_ids": [data.item_ids]}
            _data["items"] = [MODEL_MAP[item["model_name"]](**item) for item in _items]
            return _data
        return data

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _status = values.pop("status", None)
        if _status and _status is not None:
            values["msg_status"] = _status

        _action = values.pop("action", None)
        if _action is not None:
            values["msg_action"] = _action

        _type = values.pop("type", None)
        if _type and _type is not None:
            values["msg_type"] = _type

        _task = values.pop("task", None)
        if _task and _task is not None:
            values["msg_task"] = _task

        _entity = values.pop("entity", None)
        if _entity and _entity is not None:
            values["msg_entity"] = _entity

        _entity_type = values.pop("entityType", None)
        if _entity_type and _entity_type is not None:
            values["msg_entity_type"] = _entity_type

        return values


class UIObservableResponse(_Observable):
    def __init__(self, *args, **kwargs):
        # handle docs and revisions
        kwargs["data"] = self._cast_data(kwargs["data"], kwargs["msg_type"])
        super().__init__(*args, **kwargs)

    def _cast_data(self, data, msg_type):
        _items = data.items
        if _items and isinstance(_items, list):
            _data = {"item_ids": data.item_ids}
            if msg_type == "index":
                _data["totalItems"] = len(data.item_ids)
            else:
                _data["items"] = [
                    MODEL_MAP[item["model_name"]](**item) for item in _items
                ]
            return _data
        return data

    # class Config:
    #     fields = {
    #         "extra": Extra.ignore,
    #         "msg_status": "status",
    #         "msg_action": "action",
    #         "msg_type": "type",
    #         "msg_task": "task",
    #         "msg_entity": "entity",
    #         "msg_entity_type": "entityType",
    #     }

    # @validator("data")
    # def validate_data(cls, data, values):
    #     msg_entity = values.get("msg_entity", None)

    #     if msg_entity and data.items is not None:
    #         if msg_entity == "doc":
    #             data.items = [UIDoc(**item) for item in data.items]
    #     return data

    @root_validator(pre=True)
    def convert_fields(cls, values):
        _status = values.pop("status", None)
        if _status and _status is not None:
            values["msg_status"] = _status

        _action = values.pop("action", None)
        if _action is not None:
            values["msg_action"] = _action

        _type = values.pop("type", None)
        if _type and _type is not None:
            values["msg_type"] = _type

        _task = values.pop("task", None)
        if _task and _task is not None:
            values["msg_task"] = _task

        _entity = values.pop("entity", None)
        if _entity and _entity is not None:
            values["msg_entity"] = _entity

        _entity_type = values.pop("entityType", None)
        if _entity_type and _entity_type is not None:
            values["msg_entity_type"] = _entity_type

        return values

    # format json output for the ui
    def dict(self, *args, **kwargs):
        json_out = super().dict(*args, **kwargs)
        json_out["action"] = self.msg_action
        json_out["status"] = self.msg_status
        json_out["type"] = self.msg_type
        json_out["task"] = self.msg_task
        json_out["entity"] = self.msg_entity
        json_out["entityType"] = self.msg_entity_type

        json_out.pop("msg_action", None)
        json_out.pop("msg_status", None)
        json_out.pop("msg_type", None)
        json_out.pop("msg_task", None)
        json_out.pop("msg_entity", None)
        json_out.pop("msg_entity_type", None)

        return json_out
