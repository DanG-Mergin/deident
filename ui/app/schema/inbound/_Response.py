from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Optional
from pydantic import BaseModel, Field, Json


class _Response(BaseModel):
    service_name = str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID] #from the UI for example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    data: Optional[Json[Any]]#TODO: ensure this field is of some type of schema
    type: str #TODO: make this an enforced enum
    host_name: str #TODO: make this an enforced enum

    # @classmethod
    # def from_msg(msg: InternalMsg, host_name):
    #     # trust internal objects
    #     req_id, orig_id, type, data = msg
    #     host_name = host_name

    # TODO: add validators where appropriate