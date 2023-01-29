import sys
sys.path.append("..")
from ._Response import _Response
from typing import Any, Dict, Optional

# TODO: does nothing for now
class DeIdentResponse(_Response):
    data: Optional[Dict]