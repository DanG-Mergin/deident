from __future__ import annotations

from typing import Any, List, Optional
import sys

sys.path.append("...")
# TODO: define generic transmissable classes
from pydantic import ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance
from .Vocab import VocabItem
from ...services.utils import cast_to_class


class Doc(VocabItem):
    id: str
    text: str
    entities: List[EntityInstance]
    tokens: List[Token]

    @validator("entities", pre=True)
    def cast_entities(cls, e_list):
        v = []
        for e in e_list:
            if not isinstance(e, EntityInstance):
                v.append(
                    cast_to_class(
                        e,
                        EntityInstance,
                        token_ids={"start": e.start, "end": e.end},
                    )
                )
            else:
                v.append(e)
        return v
