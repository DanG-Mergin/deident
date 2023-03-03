# import scispacy
import spacy
from .utils import cast_to_class
from ..schema.messages.inbound.DeIDRequest import DeIDRequest
from ..schema.nlp.spacy.Doc import Doc as SpacyDoc
from ..schema.nlp.Doc import Doc
from typing import List, Type

# TODO: inject the pipeline
# https://spacy.io/usage/processing-pipelines
nlp = spacy.load("en_core_sci_sm")


async def deID(req: DeIDRequest) -> List[Type[Doc]]:
    annotated = []

    for doc in req.docs:
        # TODO: handle failure conditions.  One is text with no entities
        _doc = nlp(doc.text)

        s_doc = SpacyDoc(
            ents=_doc.doc.ents,
            text=_doc.doc.text,
            tokens=[token for token in _doc],
            uuid=doc.uuid,
        )
        b_doc = cast_to_class(s_doc, Doc)
        # b_doc = Doc(**s_doc.dict())
        annotated.append(b_doc)
    return annotated
