from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Extra, Field, Json


class _Response(BaseModel, extra=Extra.ignore):
    uuid: UUID
    # orig_id: Optional[str]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    data: Optional[Dict]
    error: Optional[Dict]  # for sharing additional error data
