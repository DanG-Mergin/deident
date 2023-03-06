import os
import sys
from typing import List, Dict
from uuid import UUID, uuid4
from pydantic import Extra, root_validator
from .Observable import _Observable

# from ...messages.inbound.Doc import Doc
from ..base.entities._Doc import _Doc
from ..base.messages._MessageEnums import O_Status, O_Action, O_Type, UI_Entity

# socket request for deIDification
class SocDeIDRequest(_Observable, extra=Extra.ignore):
    # TODO: add data class
    # data: Dict[str, List[_Doc]]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values
