from typing import Any, List, Optional
from pydantic import BaseModel, ValidationError, validator, root_validator
from ._Lemma import _Lemma


# An individual token — i.e. a word, punctuation symbol, whitespace, etc.
# https://spacy.io/api/token
class _Token(BaseModel):
    model_name: str = "token"
    text: str
    start_char: int
    end_char: int
    index: int
    # TODO: the id is an index
    id: int
    lemma: Optional[_Lemma]
    whitespace: Optional[str]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        spacesAfter = values.pop("spacesAfter", None)
        if spacesAfter is not None and spacesAfter > 0:
            values["whitespace"] = " " * spacesAfter

        if "text" not in values:
            raise ValueError("text is a required field")
        if not isinstance(values["text"], str):
            raise ValueError("text must be a string")
        if "start_char" not in values:
            raise ValueError("start_char is a required field")
        if not isinstance(values["start_char"], int):
            raise ValueError("start_char must be an integer")
        if "end_char" not in values:
            raise ValueError("end_char is a required field")
        if not isinstance(values["end_char"], int):
            raise ValueError("end_char must be an integer")
        if "index" not in values:
            raise ValueError("index is a required field")
        if not isinstance(values["index"], int):
            raise ValueError("index must be an integer")
        if "id" not in values:
            raise ValueError("id is a required field")

        return values
