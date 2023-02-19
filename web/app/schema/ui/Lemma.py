from typing import Dict, List, Optional, Type
from ..nlp.Vocab import VocabItem


class Lemma(VocabItem):
    id: Optional[str]
    text: str
