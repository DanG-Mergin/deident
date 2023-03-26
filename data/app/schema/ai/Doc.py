from uuid import uuid4
from datetime import datetime
from dateutil.parser import isoparse
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator

from ..base.entities._Doc import _Doc
from .Entity import NER_Entity


class NER_Doc(_Doc, extra=Extra.ignore):
    entities: List[NER_Entity]
    tokens: Optional[List[Dict]] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokens = None
        self.model_name = "ner_doc"

    @staticmethod
    async def convert_from_base(d: _Doc):
        doc = {
            **d.dict(),
        }
        doc["entities"] = [await NER_Entity.convert_from_base(e) for e in d.entities]
        return NER_Doc(**doc)
