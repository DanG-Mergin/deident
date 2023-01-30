from typing import Dict, List, Optional, Type
from pydantic import BaseModel
import sys

sys.path.append("..")
from .Vocab import VocabItem
from .Span import Span
from .Token import Token


class EntityLabel(BaseModel):
    extra = "forbid"
    kb_id: str  # points to a description of the entity
    text: str
    # description: str


class EntityInstance(VocabItem):
    id: str
    # TODO: make this a list of IDs
    # entities: List[
    #     Type["EntityInstance"]
    # ] = []  # because a span can have multiple entities
    label: EntityLabel  # TODO: this should just be IDs
    # tokens: List[Token]  # TODO: this should just be IDs
