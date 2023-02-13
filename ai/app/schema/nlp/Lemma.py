# This Lemma should contain no model/framework specific concepts

from typing import Dict, List, Optional, Type

# from pydantic import BaseModel
from .Vocab import VocabItem

# import sys

# sys.path.append("..")


class Lemma(VocabItem):
    id: Optional[str]
    text: str
