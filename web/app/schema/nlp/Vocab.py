from typing import Any, List, Optional
from pydantic import BaseModel


class VocabItem(BaseModel):
    extra = "forbid"
    id: str
