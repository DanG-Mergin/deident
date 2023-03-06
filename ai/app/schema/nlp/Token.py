from typing import Any, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator
from ..base.entities._Token import _Token
from ..base.entities._Lemma import _Lemma


# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(_Token, extra=Extra.ignore):
    @root_validator(pre=True)
    def convert_fields(cls, values):
        whitespace = values.pop("whitespace_", None)
        if whitespace:
            values["whitespace"] = whitespace

        lemma = values.pop("lemma", None)
        lemma_ = values.pop("lemma_", None)
        if lemma and lemma_:
            values["lemma"] = _Lemma(id=lemma, text=lemma_)
        return values
