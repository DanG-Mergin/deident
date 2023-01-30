from typing import Any, List, Optional

import sys

sys.path.append("..")
from .Vocab import VocabItem
from .Lemma import Lemma

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(VocabItem):
    text: str
    start: int
    end: int
    id: str
    lemma: Optional[Lemma]
