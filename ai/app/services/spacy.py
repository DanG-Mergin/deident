import sys

sys.path.append("..")
from ..data_models.spacy import EntityRecogRequest
import scispacy
import spacy

# TODO: add an environment variable to shut this off outside of dev
# import en_core_sci_sm  # simple spacy pipeline for dev and testing of some features

# TODO: develop spacy entity definition and use it prior to finalizing architecture
# https://spacy.io/usage/processing-pipelines
nlp = spacy.load("en_core_sci_sm")


async def deident(req):
    _doc = nlp(
        "Patient Dan Goldberg called in from 617-123-8899 complaining of acute lack of synthetic data."
    )
    raise Exception("debug me")
    return _doc


# TODO: define model for pipeline requests
# def deidentify(req: EntityRecogRequest):
#     # TODO: build injection mechanism for nlp model
#     _doc = nlp(req.doc)
#     return _doc


# def get_data(doc: Doc) -> Dict[str, Any]:
#     """Extract the data to return from the REST API given a Doc object. Modify
#     this function to include other data."""
#     ents = [
#         {
#             "text": ent.text,
#             "label": ent.label_,
#             "start": ent.start_char,
#             "end": ent.end_char,
#         }
#         for ent in doc.ents
#     ]
#     return {"text": doc.text, "ents": ents}
