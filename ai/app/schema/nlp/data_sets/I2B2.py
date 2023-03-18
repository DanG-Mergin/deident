from typing import Optional

from pydantic import BaseModel

# TODO: evaluate if this is the standard base case for entities
# TODO: unoptional this ish
class I2B2_Entity(BaseModel):
    model_name = "i2b2_entity"
    category: Optional[str] = None  # TODO: enum or class
    type: Optional[str] = None  # TODO: enum or class
    id: Optional[str] = None
    start: Optional[int] = None
    end: Optional[str] = None
    text: Optional[str] = None

    # TODO: add validation

    # NOTE: this data is completely fabricated aside from category and type
    class Config:
        schema_extra = {
            "example": {
                "category": "id",
                "type": "medicalrecord",
                "id": "Z8",
                "start": "135",
                "end": "145",
                "text": "171-69-77-21",  # Doesn't contain information on whitespaces
            }
        }
