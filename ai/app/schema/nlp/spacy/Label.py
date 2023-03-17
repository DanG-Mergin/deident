from uuid import uuid4
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Extra, Field, ValidationError, validator, root_validator


class NER_Label(BaseModel, extra=Extra.ignore):
    model_name = "ner_label"
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    name = "ner_label"
    category: str
    subcategory: str
