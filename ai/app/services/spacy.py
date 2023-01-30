import sys

sys.path.append("..")
# import scispacy
import spacy
from .utils import cast_to_class
from ..schema.inbound.DeIdentRequest import DeIdentRequest
from ..schema.nlp.spacy.Doc import Doc as SpacyDoc
from ..schema.nlp.Doc import Doc
from typing import List, Type

# TODO: inject the pipeline
# https://spacy.io/usage/processing-pipelines
nlp = spacy.load("en_core_sci_sm")


async def deident(req: DeIdentRequest) -> List[Type[Doc]]:
    annotated = []
    for doc in req.docs:
        _doc = nlp(doc)
        s_doc = SpacyDoc(ents=_doc.doc.ents)
        b_doc = cast_to_class(s_doc, Doc)
        annotated.append(b_doc)
    return annotated
