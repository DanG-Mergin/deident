from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator
from ...base.entities._Corpus import _Corpus
from .Doc import NER_Doc
from .Label import NER_Label


class NER_Corpus(_Corpus, extra=Extra.ignore):
    docs: List[NER_Doc]

    def __init__(self, **kwargs):
        _doc_types = kwargs.get("doc_types", [])
        if "ner" not in _doc_types:
            _doc_types.append("ner")
            kwargs["doc_types"] = _doc_types

        _model_name = kwargs.get("model_name", None)
        if _model_name and _model_name == "_corpus":
            if kwargs.get("docs", None) is not None and len(kwargs["docs"]) > 0:
                kwargs["docs"] = [
                    NER_Doc(
                        **d,
                    )
                    for d in kwargs["docs"]
                ]
            else:
                raise ValueError("docs must be a list of Doc objects")

        super().__init__(**kwargs)
        self.model_name = "ner_corpus"

    def add_docs(self, docs: List[NER_Doc]):
        self.docs.extend([NER_Doc(**d) for d in docs])

    def to_training_data(self):
        return [d.to_training_data() for d in self.docs]
