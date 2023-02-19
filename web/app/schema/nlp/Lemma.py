from typing import Dict, List, Optional, Type

from .Vocab import VocabItem


class Lemma(VocabItem):
    id: Optional[str]
    text: str
