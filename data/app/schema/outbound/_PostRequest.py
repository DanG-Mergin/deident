import sys

sys.path.append("..")
from ._Request import _Request


class _PostRequest(_Request):
    method: str
    method = "POST"
