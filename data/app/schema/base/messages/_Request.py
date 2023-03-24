from pydantic import Extra
from ._Message import _Message


class _Request(_Message, extra=Extra.allow):
    method: str = "POST"
    base_url: str = ""

    @property
    def url(self):
        return self.base_url

    @url.setter
    def url(self, value):
        self.base_url = value
