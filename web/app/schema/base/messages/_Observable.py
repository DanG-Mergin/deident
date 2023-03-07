from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, Union
from pydantic import (
    Extra,
)
from ._Message import _Message


class _Observable(_Message, extra=Extra.ignore):
    # uuid: str = Field(default_factory=lambda: str(uuid4()))
    # msg_action: str
    # msg_status: str
    msg_type: str
    # msg_task: Optional[str]
    msg_entity: str
    msg_entity_type: str
    # data: Union[_Data, Dict[str, Any], None, Dict]
