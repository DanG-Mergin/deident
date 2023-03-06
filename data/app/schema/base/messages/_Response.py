from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json
from ._Data import _Data


class _Response(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    # orig_id: Optional[str]  # from the webfor example
    data: Optional[_Data]
    # data: Optional[Dict]
