from pydantic import root_validator
from ._Message import _Message

# Currently this wrapper provides no value except to allow for easier handling of special cases
# as implemented on the web side.  It may be removed in the future.s
class _Response(_Message):
    @root_validator(pre=True)
    def convert_fields(cls, values):

        return values
