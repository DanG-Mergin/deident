from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json 
import sys
sys.path.append("..")
from .. import InternalMsg


class _Request(BaseModel):
    # service_name: str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID] #from the UI for example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]] #TODO: ensure this field is of some type of schema
    data: Optional[Dict]
    meta_type: str #TODO: make this an enforced enum
    host_name: str #TODO: make this an enforced enum

    @staticmethod 
    def from_obj(obj: BaseModel, **kwargs):
        attr = {k: v for k, v in obj.__dict__.items()}
        return _Request(**attr, **kwargs)
    
    # @classmethod
    # def from_msg(self, msg: InternalMsg, host_name):
    #     # trust internal objects
    #     self.req_id, self.orig_id, self.type, self.data = msg
    #     self.host_name = host_name

    # TODO: add validators where appropriate

