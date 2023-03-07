from pydantic import Extra
from ._Message import _Message


class _Request(_Message, extra=Extra.allow):
    method: str = "POST"
    _url: str = ""

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
