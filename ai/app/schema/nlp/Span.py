# This span should contain no model/framework specific concepts

from typing import Dict, List, Optional, Type


import sys

sys.path.append("..")
from .Vocab import VocabItem


class Span(VocabItem):
    extra = "forbid"
    # text: str
    start: int  # 0 indexed by presumed token including whitespace and punctuation
    end: int  # 0 indexed by presumed token including whitespace and punctuation, first token AFTER the span
    type: str
