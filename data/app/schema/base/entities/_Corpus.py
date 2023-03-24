from uuid import uuid4
from datetime import datetime
from dateutil.parser import isoparse
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

from ._Doc import _Doc
from ._Label import _Label

# from ....services.request import bulk_get_documents


class _Corpus(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    model_name = "_corpus"
    doc_types: List[str] = ["all"]
    tasks: List[str] = ["all"]
    patient_classes: Optional[List[str]]
    doc_ids: Optional[List[str]]
    docs: Optional[List[_Doc]]
    # label_ids: Optional[List[str]]
    labels: Optional[List[_Label]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if kwargs["should_hydrate"] and kwargs["should_hydrate"] is True:
        #     self.hydrate()

    @property
    def label_ids(self):
        if self.docs is not None:
            return list(set(label for doc in self.docs for label in doc.label_ids))
        return []

    @validator("created_at")
    def iso8601_date(cls, v):
        """
        Converts the created_at string to an ISO 8601 formatted string for elastic.
        """
        dt = isoparse(v)
        return dt.isoformat()

    # async def hydrate(self):
    #     _docs_req = await bulk_get_documents("doc", self.doc_ids)
    #     self.docs = [_Doc(d) for d in _docs_req]
    #     # label_ids = self.label_ids
    #     _labels_req = await bulk_get_documents("label", self.label_ids)
    #     self.labels = [_Label(l) for l in _labels_req]

    #     # get the doc_ids from the corpus

    #     # get the docs from the doc_ids
    #     # get the labels from the docs
    #     # return a new corpus with the docs and labels
    #     pass
