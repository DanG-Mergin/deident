from ...services.elastic.dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()

from ...services.elastic import request
from ._RequestCtrl import _RequestCtrl
from ...schema.base.entities._Doc import _Doc


class DocCtrl(_RequestCtrl):
    @classmethod
    async def update_document(self, index, document_id, document: _Doc, es=_es):
        print("DocCtrl might want to update the corpus here")
        res = await request.update_document(index, document_id, document.dict(), es)
        return res

    @classmethod
    async def create_document(self, index, document_id, document: _Doc, es=_es):
        print("DocCtrl should be updating the corpus document_ids here")
        # get corpora with matching meta tags
        # TODO: do we want saved corpus objects or just views?
        res = await request.create_document(index, document_id, document.dict(), es)
        return res

    @classmethod
    async def delete_document(self, index, document_id, es=_es):
        print("DocCtrl should be updating the corpus document_ids here")
        res = await request.delete_document(index, document_id, es)
        return res
