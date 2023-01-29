import os
import sys

sys.path.append("..")
from ._PostRequest import _PostRequest


class DeIdentRequest(_PostRequest):
    service_name = "deident"
    url = f"{os.environ['AI_DEIDENT_URL']}"
