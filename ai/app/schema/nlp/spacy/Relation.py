from typing import Any, List, Optional

from pydantic import BaseModel
from .Span import HeadSpan, ChildSpan


class Relation(BaseModel):
    head: int
    child: int
    head_span: HeadSpan
    child_span: ChildSpan
    color: str
    label: str
