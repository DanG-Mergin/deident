from typing import Optional, List

from pydantic import BaseModel
from ...base.entities._Entity import _Entity
from ...base.entities._Doc import _Doc

# TODO: what are we doing with Corpora?  Saving or just using views?
from ..spacy.Corpus import NER_Corpus
from ..spacy.Doc import NER_Doc
from ..spacy.Entity import NER_Entity
from ....services import label as label_svc


# TODO: unoptional this ish
class I2B2_Entity(_Entity):
    model_name = "i2b2_entity"
    category: Optional[str]
    type: Optional[str]
    id: Optional[str] = None
    # label_id: Optional[str] = None
    start: Optional[int]
    end: Optional[str]
    text: Optional[str] = None

    # def __init__(self, **kwargs):

    #     super().__init__(**kwargs)

    class Config:
        schema_extra = {
            "example": {
                "category": "name",
                "type": "patient",
                "id": "Z8",
                "start": "135",
                "end": "145",
                "text": "171-69-77-21",  # Doesn't contain information on whitespaces
            }
        }

    def __dict__(self):
        return {
            "category": self.category,
            "subcategory": self.type,
            "id": self.id,
            "start_char": self.start,
            "end_char": self.end,
            "text": self.text,
        }


class I2B2_Doc(NER_Doc):
    model_name = "i2b2_doc"
    tokens = None

    def __init__(self, **kwargs):
        _ents = [I2B2_Entity(**e) for e in kwargs["entities"]]
        kwargs["entities"] = self._ingest_entities(_ents)
        super().__init__(**kwargs)
        # self.model_name = "i2b2_doc"

    # NOTE: currently we are only mapping these entities to the needs of spacy
    # not the UI/db as i2b2 shouldn't show up in the UI, and we aren't saving it
    async def _ingest_entities(self, entities: List[I2B2_Entity]):
        _ents = [e.dict() for e in entities]
        labeled_ents = await label_svc.get_labels_by_props(_ents)
        return labeled_ents


# class I2B2_Corpus(NER_Corpus):
#     def __init__(self, **kwargs):
#         # take a list of docs and i2b2 entities

#         super().__init__(**kwargs)
#         self.model_name = "i2b2_corpus"
