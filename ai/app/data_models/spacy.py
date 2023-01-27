# spacy.py contains all types relating to spacy.
# it may of course make sense to split this up if "things get complicated"
from typing import Dict, List, Optional
from pydantic import BaseModel

# TODO: review fields and requirements
# TODO: move optional/not into validator
class SpacyModel(BaseModel):
    name: str
    # TODO: rethink this classification
    type: str
    application: str
    # TODO: architecture... may be handled by uuid and db/config/other service
    uri: Optional[str]
    components: Optional[List[str]]
    # TODO: change this to uuid data type?
    uuid: Optional[str]
    specialties: Optional[List]

    # TODO: add validation

    class Config:
        schema_extra = {
            "example": {
                "name": "en_core_web_sm",
                "type": "pipeline",
                "application": "NER",
                "uri": "//something or something.something...  TBD",
                "components": ["tokenizer", "tagger", "en_core_lg", "custom_model"],
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "specialties": ["general", "allergy", "oncology"],
            }
        }


# TODO: define message protocol
class EntityRecogRequest(BaseModel):
    doc: str
    # TODO: does this belong here?  the idea is to use it for formatting the UI output
    # -- however that work probably belongs in the front end so that entities can be toggled on and off
    entities: List[str]

    class Config:
        schema_extra = {
            "example": {
                "doc": "Hello I am a named entity request string",
                "entities": ["phi"],
            }
        }


# TODO: define message protocol
class EntityRecogResponse(BaseModel):
    doc: str
    entities: List[str]

    class Config:
        schema_extra = {
            "example": {
                "doc": "Hello I am a named entity request string",
                "entities": ["phi"],
            }
        }


# TODO: we may not need these granular entities defined on the API... only io with spacy or regards spacy
# class span

# class Example(BaseModel):
#     text: str
#     words: List[str]
#     lemmas: List[str]
#     spaces: List[bool]
#     tags: List[str]
#     pos: List[str]
#     morphs: List[str]
#     sent_starts: List[Optional[bool]]
#     deps: List[str]
#     heads: List[int]
#     entities: List[str]
#     entities: List[(int int str)]
#     cats: Dict[str float]
#     links: Dict[(int int) dict]
#     spans: Dict[str List[Tuple]]
