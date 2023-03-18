from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator
from ...base.entities._Corpus import _Corpus
from .Doc import NER_Doc
from .Label import NER_Label


class NER_Corpus(_Corpus, extra=Extra.ignore):
    docs: List[NER_Doc]
    labels: List[NER_Label]

    def __init__(self, **kwargs):
        self.types.append("ner")
        # if casting from
        if kwargs["model_name"] == "_corpus":

            if kwargs["labels"] is not None and len(kwargs["labels"]) > 0:
                kwargs["labels"] = [NER_Label(l) for l in kwargs["labels"]]
            else:
                raise ValueError("labels must be a list of Label objects")

            if kwargs["docs"] is not None and len(kwargs["docs"]) > 0:
                kwargs["docs"] = [
                    NER_Doc(
                        entities=d.entities,
                        text=d.text,
                        tokens=d.tokens,
                        labels=kwargs["labels"],
                    )
                    for d in kwargs["docs"]
                ]
            else:
                raise ValueError("docs must be a list of Doc objects")

        super().__init__(**kwargs)
        self.model_name = "ner_corpus"
