from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json


class _Response(BaseModel):
    service_name = str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID] #from the UI for example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]]#TODO: ensure this field is of some type of schema
    data: Optional[Dict]
    type: str #TODO: make this an enforced enum

    # TODO: this should be an __init__ if we don't get other use cases
    @staticmethod 
    def from_obj(obj: BaseModel, **kwargs):
        attr = {k: v for k, v in obj.__dict__.items()}
        return _Response(**attr, **kwargs)
    # TODO: add validators where appropriate