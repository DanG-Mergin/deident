from pydantic import BaseModel, Field, Extra
import sys

sys.path.append("..")
from ._Request import _Request


class _PostRequest(_Request, extra=Extra.allow):
    method: str
    method = "POST"
