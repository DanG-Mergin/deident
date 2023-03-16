from ...services.elastic.dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()

from ...services.elastic import request
from ._RequestCtrl import _RequestCtrl
from ...schema.base.entities._Doc import _Doc


class DocCtrl(_RequestCtrl):
    @classmethod
    async def update_document(self, index, document_id, document: _Doc, es=_es):
        res = await request.update_document(index, document_id, document.dict(), es)
        return res

    @classmethod
    async def create_document(self, index, document_id, document: _Doc, es=_es):
        res = await request.create_document(index, document_id, document.dict(), es)
        return res

    @classmethod
    async def delete_document(self, index, document_id, es=_es):
        res = await request.delete_document(index, document_id, es)
        return res
