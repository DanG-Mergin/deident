from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field
from ....schema.inbound.Doc import Doc as InboundDoc


class Doc(InboundDoc):
    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values
