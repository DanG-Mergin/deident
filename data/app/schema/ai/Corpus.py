from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator
from .Doc import NER_Doc, DRUG_Doc
from ..base.entities._Doc import _Doc


class NER_Corpus(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    model_name = "ner_corpus"
    docs: List[NER_Doc]

    # this seems necessary given that pydantic doesn't support async validators
    @staticmethod
    async def convert_docs(docs: List[_Doc]):
        return [await NER_Doc.convert_from_base(d) for d in docs]

    def add_docs(self, docs: List[NER_Doc]):
        self.docs.extend([NER_Doc(**d) for d in docs])


class DRUG_Corpus(BaseModel, extra=Extra.ignore):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    model_name = "drug_corpus"
    docs: List[DRUG_Doc]

    # this seems necessary given that pydantic doesn't support async validators
    @staticmethod
    async def convert_docs(docs: List[_Doc]):
        return [await DRUG_Doc.convert_from_base(d) for d in docs]

    def add_docs(self, docs: List[DRUG_Doc]):
        self.docs.extend([DRUG_Doc(**d) for d in docs])
