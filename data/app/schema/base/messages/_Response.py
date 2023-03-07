from pydantic import root_validator
from ._Message import _Message


class _Response(_Message):
    @root_validator(pre=True)
    def convert_fields(cls, values):

        return values
