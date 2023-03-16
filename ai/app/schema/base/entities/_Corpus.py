from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

from ._Doc import _Doc
from ._Label import _Label


class _Corpus(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow()))
    name = "_corpus"
    doc_types: List[str] = ["all"]
    tasks: List[str] = ["all"]
    patient_classes: Optional[List[str]]
    doc_ids: Optional[List[str]]
    docs: Optional[List[_Doc]]
    labels: Optional[List[_Label]]
    should_hydrate: bool = False

    def __init__(self, **kwargs):
        # if kwargs["labels"] is not None and len(kwargs["labels"]) > 0:
        #     kwargs["labels"] = [_Label(l) for l in kwargs["labels"]]
        # else:
        #     raise ValueError("labels must be a list of Label objects")

        # if kwargs["docs"] is not None and len(kwargs["docs"]) > 0:
        #     kwargs["docs"] = [
        #         NER_Doc(
        #             entities=d.entities,
        #             text=d.text,
        #             tokens=d.tokens,
        #             labels=kwargs["labels"],
        #         )
        #         for d in kwargs["docs"]
        #     ]
        # else:
        #     raise ValueError("docs must be a list of Doc objects")

        super().__init__(**kwargs)
