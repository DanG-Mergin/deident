from typing import Any, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator

from .Lemma import Lemma

# from ..nlp.Lemma import Lemma

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(BaseModel, extra=Extra.ignore):
    text: str
    index: int
    # TODO: the id is an entity id, not a token id
    id: str
    lemma: Optional[Lemma]
    spacesAfter: Optional[int]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        whitespace = values.pop("whitespace", None)
        if whitespace:
            values["spacesAfter"] = len(whitespace)
        else:
            values["spacesAfter"] = 0

        return values
