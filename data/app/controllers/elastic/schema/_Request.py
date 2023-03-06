from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, Extra, ValidationError, validator, root_validator

# import sys

# sys.path.append("..")


class _Request(BaseModel, extra=Extra.allow):
    # service_name: str #TODO: make this an enforced enum
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    # orig_id: Optional[str]  # from the webfor example
    data: Optional[Dict]
