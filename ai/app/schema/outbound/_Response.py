from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json


class _Response(BaseModel):
    extra = "ignore"
    req_id: UUID
    orig_id: Optional[UUID]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]]#TODO: ensure this field is of some type of schema
    data: Optional[Dict]
    error: Optional[Dict]  # for sharing additional error data

    # TODO: add validators where appropriate
