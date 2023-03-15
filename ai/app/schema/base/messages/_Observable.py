from typing import Any, Dict, Optional, Type, Union
from pydantic import (
    Extra,
)
from ._Message import _Message


class _Observable(_Message, extra=Extra.ignore):
    msg_type: str
    msg_entity: str
    msg_entity_type: str
