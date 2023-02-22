from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json


class _Response(BaseModel):
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
