from ...schema.base.entities._Corpus import _Corpus
from ...schema.base.entities._Doc import _Doc
from ...schema.base.entities._Label import _Label
from .request import bulk_get_documents

# a controller or service uses methods in this service
# to construct composite objects and retrieve fields as
# needed.  A design choice for this project is to not make requests
# from objects/entities to external services/controllers
def hydrate(corpus: _Corpus) -> _Corpus:
    # get the doc_ids from the corpus
    # NOTE: we assume that the corpus has already been searched based on
    # the types and filters, and that the doc_ids are already populated
    # doc_query = {
    #   "query": {
    #     "match"
    _docs_req = bulk_get_documents("doc", corpus.doc_ids)
    corpus.docs = [_Doc(d) for d in _docs_req]
    label_ids = corpus.label_ids
    _labels_req = bulk_get_documents("label", label_ids)
    corpus.labels = [_Label(l) for l in _labels_req]
    return corpus
