from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, Optional
from pydantic import BaseModel, Extra, Field, Json
import sys

sys.path.append("..")


class _Request(BaseModel, extra=Extra.ignore):
    req_id: str = Field(default_factory=lambda: str(uuid4()))
    orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
