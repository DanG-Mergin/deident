import sys
sys.path.append("..")
from ._Request import _Request

# TODO: conform to general post request data format
class _PostRequest(_Request):
    req_type: str
    req_type = "post"
