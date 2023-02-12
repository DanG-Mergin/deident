from typing import Any, List, Optional

from pydantic import BaseModel

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(BaseModel):
    text: str
    start_char: int
    end_char: int
    id: int
