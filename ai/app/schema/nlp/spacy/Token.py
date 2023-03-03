from typing import Any, List, Optional

from pydantic import BaseModel, Extra

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(BaseModel, extra=Extra.ignore):
    text: str
    start_char: int
    end_char: int
    index: int
    id: int  # id is the index of the token
    lemma: Optional[str]
    lemma_: Optional[str]
    whitespace_: Optional[str]
