# for all base model custom message schema
from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json
from pydantic.dataclasses import dataclass

# inbound and outbound messages must be converted to maintain
# separation of concerns.  Breaking this rule gets really ugly
# over time as abstractions leak.  The only truely persistent
# value should ideally be the id to keep track of async ops

class InternalMsg(BaseModel):
    ui_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID] #from the UI for example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]] #TODO: ensure this field is of some type of schema
    data: Optional[Dict]
    meta_type: str #TODO: make this an enforced enum

    # TODO: add validation