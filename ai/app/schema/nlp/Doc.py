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

    # @validator("tokens")
    # def cast_tokens(cls, t_list):
    #     v = []
    #     for t in t_list:
    #         if not isinstance(t, Token):
    #             v.append(cast_to_class(t, Token))
    #         else:
    #             v.append(t)
    #     return v

    # @root_validator(pre=True)
    # def convert_fields(self, values):
    #     entities = values.pop("entities", None)
    #     if entities:
    #         for field_name in self.__fields__:
    #             if field_name in entities:
    #                 values[field_name] = entities[field_name]
    #         tokens = [Token(**t) for t in ]

    #     return values
