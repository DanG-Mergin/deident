from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Json

# import sys
# sys.path.append("..")


class _Request(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    # orig_id: Optional[str]
    data: Optional[Dict]
