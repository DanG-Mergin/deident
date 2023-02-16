from uuid import UUID, uuid4
from typing import Any, Dict, Optional, Type, List
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator
import sys

sys.path.append("..")

from pydantic import ValidationError, validator, root_validator
from .Token import Token
from .Entity import EntityInstance
from .Vocab import VocabItem
from .Entity import EntityLabel


class Doc(VocabItem):
    # TODO: need to figure out how we're keeping track of these
    id: Optional[str] = Field(default_factory=uuid4, alias="id")
    text: str
    entities: List[EntityInstance]
    tokens: List[Token]
    labels: List[EntityLabel]

    @root_validator(pre=True)
    def convert_fields(cls, values):
        #  TODO: make actual labels this is hideous
        labels = {}
        if not values.get("labels"):
            ents = values.pop("entities", None)
            if ents:
                for ent in ents:
                    if not hasattr(ent, "label") or not hasattr(ent.label, "kb_id"):
                        label_id = "100"
                    else:
                        label_id = ent.label.kb_id
                        labels[label_id] = EntityLabel(
                            kb_id=label_id, text=ent.label.text
                        )
                values["entities"] = ents
                values["labels"] = list(labels.values())
            # values["labels"] = [
            #     EntityLabel(kb_id=ent["label_id"], text=ent["text"]) for ent in ents
            # ]
        return values
