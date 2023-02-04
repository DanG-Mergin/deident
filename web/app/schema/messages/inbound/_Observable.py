from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field, Json
import sys
sys.path.append("..")
from .._MessageEnums import Status, Action


    
class _Observable(BaseModel):
    req_id: UUID = Field(default_factory=uuid4)
    orig_id: Optional[UUID]  # from the ui for example
    action: Action
    status: Status
    # time_start: datetime = Field(default_factory=datetime.utcnow)
    # time_end: Optional[datetime]
    data: Optional[Type[BaseModel]]

    # TODO: add validators where appropriate