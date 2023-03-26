import json
from ...services.elastic.dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()

from ...services.elastic import request

# generic request controller to provide middleware for entity specific operations
# - such as updating a corpus document_ids when a document is created or deleted
class _RequestCtrl:
    # @staticmethod
    def _filter_none_values(document):
        _document = {k: v for k, v in document.items() if v is not None}
        return _document

    @classmethod
    async def create_document(self, index, document_id, document, es=_es):
        return await request.create_document(index, document_id, document.dict(), es)

    @classmethod
    async def update_document(self, index, document_id, document, es=_es):
        # remove None values from the document so we aren't nulling out fields
        _document = {k: v for k, v in document.dict().items() if v is not None}
        # json_doc = json.dumps(_document)
        return await request.update_document(index, document_id, _document, es)

    @classmethod
    async def get_index(self, index, es=_es):
        return await request.get_index(index, es)

    @classmethod
    async def get_document(self, index, document_id, es=_es):
        return await request.get_document(index, document_id, es)

    @classmethod
    async def get_document_by_id(self, index, document_id, es=_es):
        return await request.get_document_by_id(index, document_id, es)

    @classmethod
    async def delete_document(self, index, document_id, es=_es):
        return await request.delete_document(index, document_id, es)

    @classmethod
    async def search_documents(self, index, req, es=_es):
        return await request.search_documents(index, req.query, es)

    @classmethod
    async def bulk_create_documents(self, index, documents, es=_es):
        return await request.bulk_create_documents(index, documents, es)

    @classmethod
    async def bulk_get_documents(self, index, document_ids, es=_es):
        return await request.bulk_get_documents(index, document_ids, es)

    @classmethod
    async def bulk_update_documents(self, index, documents, es=_es):
        return await request.bulk_update_documents(index, documents, es)

    @classmethod
    async def bulk_delete_documents(self, index, document_ids, es=_es):
        return await request.bulk_delete_documents(index, document_ids, es)
