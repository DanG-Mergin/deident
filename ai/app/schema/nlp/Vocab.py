from typing import Any, List, Optional
from pydantic import BaseModel, Extra


class VocabItem(BaseModel, extra=Extra.ignore):
    id: str
