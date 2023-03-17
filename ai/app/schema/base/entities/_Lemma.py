from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator


class _Lemma(BaseModel):
    model_name: str = "lemma"
    id: Optional[str]
    text: str
