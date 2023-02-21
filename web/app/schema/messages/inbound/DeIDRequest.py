import os
import sys
from typing import List, Dict
from uuid import UUID, uuid4
from pydantic import ValidationError, validator, root_validator, BaseModel, Field

sys.path.append("..")
from ._Observable import _Observable
from .nlp.Doc import Doc
from .._MessageEnums import O_Status, O_Action, O_Type, UI_Entity

# socket request for deIDification
class SocDeIDRequest(_Observable):
    extra = "ignore"
    data: Dict[str, List[Doc]]
