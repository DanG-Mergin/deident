# This Lemma should contain no model/framework specific concepts

from typing import Dict, List, Optional, Type
from pydantic import BaseModel

# import sys

# sys.path.append("..")


class Lemma(BaseModel):
    extra = "forbid"
    id: Optional[str]
    text: str
