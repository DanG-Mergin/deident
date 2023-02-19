from typing import Any, List, Optional
from pydantic import BaseModel, ValidationError, validator, root_validator
import sys

sys.path.append("..")
from .Vocab import VocabItem
from .Lemma import Lemma

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(VocabItem):
    text: str
    # start_char: int
    # end_char: int
    # TODO: the id is the index of the token
    index: int
    id: str
    lemma: Optional[Lemma]
    whitespace: Optional[str]

    @validator("id")
    def convert_id(cls, v):
        return str(v)

    @root_validator(pre=True)
    def convert_fields(cls, values):
        whitespace = values.pop("whitespace_", None)
        if whitespace:
            values["whitespace"] = whitespace

        lemma = values.pop("lemma", None)
        lemma_ = values.pop("lemma_", None)
        if lemma and lemma_:
            values["lemma"] = Lemma(id=lemma, text=lemma_)
        return values
