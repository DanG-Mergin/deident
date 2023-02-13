from typing import Any, List, Optional

from pydantic import BaseModel

# an ordered sequence of tokens representing a slice of a doc object
# TODO: not currently being used.  We may not need it for this project really as an entity is a type of span
class Span(BaseModel):
    text: str
    start: int
    token_start: int
    token_end: int
    end: int
    type: str
    label: str


class HeadSpan(BaseModel):
    start: int
    end: int
    token_start: int
    token_end: int
    label: str


class ChildSpan(BaseModel):
    start: int
    end: int
    token_start: int
    token_end: int
    label: str
