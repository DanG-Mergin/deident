from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Field, Json, ValidationError, validator, root_validator


class Lemma(BaseModel):
    id: Optional[str]
    text: str
