from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict, Union
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

from ._Doc import _Doc

# from ...nlp.spacy.Doc import NER_Doc
from ._Label import _Label


class _Corpus(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    model_name = "_corpus"
    doc_types: List[str] = ["all"]
    tasks: List[str] = ["all"]
    patient_classes: Optional[List[str]]
    doc_ids: Optional[List[str]]
    docs: Union[List[_Doc], List[Dict]]
    # labels: Optional[List[_Label]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
