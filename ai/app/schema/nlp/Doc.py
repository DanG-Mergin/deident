from __future__ import annotations

from typing import Any, List, Optional

# TODO: define generic transmissable classes
from pydantic import Extra, Field, ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance, EntityLabel
from ...services.utils import cast_to_class
from uuid import uuid4
from ...schema.base.entities._Doc import _Doc


class Doc(_Doc, extra=Extra.ignore):
    entities: List[EntityInstance]
    tokens: List[Token]

    @validator("entities", pre=True)
    def cast_entities(cls, e_list):
        v = []

        for e in e_list:
            if not hasattr(e, "label") or not hasattr(e.label, "kb_id"):
                label_id = None
            else:
                # TODO: this is a hack as we're only getting the kb_id for now
                label_id = "44cecac2-f305-44b3-9627-4f7d6c12db3b"

            if not isinstance(e, EntityInstance):
                v.append(
                    cast_to_class(
                        e,
                        EntityInstance,
                        label_id=label_id,
                    )
                )
            else:
                v.append(e)
        return v

    @root_validator(pre=True)
    def convert_fields(cls, values):
        return values
