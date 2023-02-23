from __future__ import annotations

from typing import Any, List, Optional
import sys

sys.path.append("...")
# TODO: define generic transmissable classes
from pydantic import ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance, EntityLabel
from .Vocab import VocabItem
from ...services.utils import cast_to_class


class Doc(VocabItem):
    id: str
    text: str
    entities: List[EntityInstance]
    tokens: List[Token]
    labels: List[EntityLabel] = []

    @validator("entities", pre=True)
    def cast_entities(cls, e_list):
        v = []
        labels = {}
        for e in e_list:
            if not hasattr(e, "label") or not hasattr(e.label, "kb_id"):
                label_id = None
            else:
                # label_id = e.label.kb_id
                # TODO: this is a hack as we're only getting the kb_id for now
                label_id = "44cecac2-f305-44b3-9627-4f7d6c12db3b"
                labels[label_id] = EntityLabel(kb_id=label_id, text=e.label.text)

            if not isinstance(e, EntityInstance):
                v.append(
                    cast_to_class(
                        e,
                        EntityInstance,
                        token_ids={"start": e.start, "end": e.end},
                        label_id=label_id,
                        start_index=e.start,
                        end_index=e.end,
                    )
                )
            else:
                v.append(e)
                v["labels"] = list(labels.values())
        return v

    # TODO: this is a hack to get around time constraints..  clean it up
    # @validator("tokens", pre=True)
    # def cast_tokens(cls, t_list):
    #     v = []
    #     try:
    #         for t in t_list:
    #             if not isinstance(t, Token):
    #                 v.append(
    #                     cast_to_class(
    #                         t,
    #                         Token,
    #                         index=t.id,
    #                     )
    #                 )
    #             else:
    #                 v.append(t)
    #         return v
    #     except Exception as e:
    #         print(e)
