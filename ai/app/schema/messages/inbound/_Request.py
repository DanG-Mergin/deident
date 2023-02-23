from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json

# import sys
# sys.path.append("..")


class _Request(BaseModel):
    method = "POST"
    req_id: str = Field(default_factory=lambda: str(uuid4()))
    orig_id: Optional[str]  # from the webfor example
    time_start: datetime = Field(default_factory=datetime.utcnow)
    time_end: Optional[datetime]
    data: Optional[Dict]

    # TODO: add validators where appropriate
