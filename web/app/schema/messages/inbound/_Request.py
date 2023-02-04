from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json

# import sys
# sys.path.append("..")


class _Request(BaseModel):
    # service_name: str #TODO: make this an enforced enum
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    # data: Optional[Json[Any]] #TODO: ensure this field is of some type of schema
    data: Optional[Dict]

    # TODO: add validators where appropriate
