from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Optional
from pydantic import BaseModel, Field, Json
import sys

sys.path.append("..")


class _Request(BaseModel):
    extra = "ignore"  # only defined properties can be set
    # service_name: str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID]  # from the UI for example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]] #TODO: ensure this field is of some type of schema
    data: Optional[Dict]
    # meta_type: str #TODO: make this an enforced enum
    # host_name: str #TODO: make this an enforced enum

    # TODO: add validators where appropriate
