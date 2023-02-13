from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Extra, Field, validator, json
import sys

sys.path.append("..")
from .._MessageEnums import O_Status, O_Action, O_Type, UI_Entity


class _Observable(BaseModel, extra=Extra.allow):
    # the alias is used to map the field name to the name used during serialzation
    _req_id: UUID = Field(default_factory=uuid4)
    orig_id: str
    o_action: str
    o_status: str
    o_type: str
    entity: str
    data: Optional[dict]

    @property
    def req_id(self):
        return str(self._req_id)

    # exclude unset fields from the serialized output
    def to_json(self) -> str:
        return json.dumps(self.dict(exclude_unset=True))
