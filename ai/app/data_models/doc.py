# doc.py contains pydantic model definitions for documents used in nlp

from pydantic import BaseModel


class Doc(BaseModel):
    text: str
    uuid: str
