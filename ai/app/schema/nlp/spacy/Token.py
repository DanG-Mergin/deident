from typing import Any, List, Optional

from pydantic import BaseModel, Extra
from ...base.entities._Token import _Token

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(_Token, extra=Extra.ignore):
    lemma: Optional[str]
    lemma_: Optional[str]
    whitespace_: Optional[str]
