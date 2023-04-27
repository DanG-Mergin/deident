# import scispacy
import os, spacy
from ..utils import cast_to_class
from pathlib import Path

from ...schema.base.entities._Doc import _Doc
from ...schema.nlp.spacy.Doc import Doc as SpacyDoc
from ...schema.nlp.Doc import Doc
from .. import label as label_svc
from typing import List, Type

# TODO: inject the pipeline
# https://spacy.io/usage/processing-pipelines
# nlp = spacy.load("en_core_sci_sm")


def _get_model_path():
    current_dir = Path(__file__).resolve().parent

    # Move up the directory tree to the ".ai" directory
    model_dir = current_dir.parents[1]
    return os.path.join(model_dir, "assets", "models")


async def deID(docs: List[Type[_Doc]]) -> List[Type[Doc]]:
    model_path = _get_model_path()
    nlp = spacy.load(f"{model_path}/en_deid_ner-0.0.0/en_deid_ner/en_deid_ner-0.0.0")

    annotated = []

    for doc in docs:
        # TODO: handle failure conditions.  One is text with no entities
        _doc = nlp(doc["text"])

        s_doc = SpacyDoc(
            ents=_doc.doc.ents,
            text=_doc.doc.text,
            tokens=[token for token in _doc],
            uuid=doc["uuid"],
        )
        # mapping labels from db to spacy output
        s_doc.entities = await s_doc.map_labels(s_doc.entities)
        print("s_doc uuid is ", s_doc.uuid)
        b_doc = cast_to_class(s_doc, Doc)
        print("b_doc uuid is ", b_doc.uuid)
        annotated.append(b_doc)
    return annotated
