from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Optional
from pydantic import BaseModel, Extra, Field, Json
import sys

sys.path.append("..")


class _Request(BaseModel, extra=Extra.ignore):
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[str]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    data: Optional[Dict]
