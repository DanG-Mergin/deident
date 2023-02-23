from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Extra, ValidationError, validator, root_validator


class _Request(BaseModel, extra=Extra.allow):
    method: str = "POST"
    req_id: str = Field(default_factory=lambda: str(uuid4()))
    orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
