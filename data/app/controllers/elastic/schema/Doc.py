from pydantic import BaseModel, ValidationError, validator, root_validator, Extra, Field
from typing import List, Optional
from ....schema.inbound.Doc import Doc as InboundDoc
from ....schema.inbound.Entity import Entity as InboundEntity
from ....schema.inbound.Token import Token as InboundToken


class Token(InboundToken):
    # label_id: str
    # ner: str
    # dep: str
    # tag: str
    # index: int
    # start_char: int
    # end_char: int
    orth: str
    whitespace: Optional[str]

    class Config:
        fields = {"orth": "text", "extra": Extra.ignore}


# class Entity(InboundEntity, extra=Extra.ignore):


class Doc(InboundDoc, extra=Extra.ignore):
    # uuid: str
    # text: str
    entities: List[InboundEntity]
    tokens: List[Token]

    @root_validator(pre=True)
    def convert_fields(cls, values):

        return values
