from pydantic import root_validator, Extra
from ._Message import _Message


class _Response(_Message, extra=Extra.ignore):
    @root_validator(pre=True)
    def convert_fields(cls, values):

        return values
