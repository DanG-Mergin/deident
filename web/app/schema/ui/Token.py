from typing import Any, List, Optional
from pydantic import BaseModel, Extra, ValidationError, validator, root_validator
from ..nlp.Vocab import VocabItem
from .Lemma import Lemma

# from ..nlp.Lemma import Lemma

# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class Token(VocabItem, extra=Extra.ignore):
    text: str
    index: int
    # TODO: the id is an entity id, not a token id
    id: str
    lemma: Optional[Lemma]
    whitespace: Optional[str]

    # @root_validator(pre=True)
    # def convert_fields(cls, values):
    #     startChar = values.pop("start_char", None)
    #     if startChar:
    #         values["startChar"] = startChar
    #     endChar = values.pop("end_char", None)
    #     if endChar:
    #         values["endChar"] = endChar

    #     return values
