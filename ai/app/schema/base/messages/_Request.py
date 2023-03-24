from pydantic import Extra, validator
from ._Message import _Message
import os


class _Request(_Message, extra=Extra.allow):
    method: str = "POST"
    base_url: str = f'{os.environ.get("DATA_URL")}'
    endpoint: str = ""

    @property
    def url(self):
        return f"{self.base_url}/{self.endpoint}"
