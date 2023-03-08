from typing import Any, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator
from ..base.entities._Token import _Token

# from ..nlp.Lemma import Lemma

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(_Token, extra=Extra.ignore):
    spacesAfter: Optional[int]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        whitespace = values.pop("whitespace", None)
        if whitespace:
            values["spacesAfter"] = len(whitespace)
        else:
            values["spacesAfter"] = 0

        return values
