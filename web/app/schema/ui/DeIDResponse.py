from typing import Dict, List
from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field

# from ..base.messages._Observable import _Observable
from ..ui.Observable import UIObservableResponse
from .Doc import Doc
from ..base.messages._Data import _Data


class SocDeIDResponse(UIObservableResponse):
    @validator("data")
    def validate_data(cls, v):
        if not v:
            raise ValueError("data must be a non-empty list")
        else:
            v.items = [Doc(**item) for item in v.items]
        return v
