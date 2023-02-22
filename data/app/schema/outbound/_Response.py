from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Extra, Field, Json


class _Response(BaseModel, extra=Extra.ignore):
    req_id: UUID
    orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
    error: Optional[Dict]  # for sharing additional error data
