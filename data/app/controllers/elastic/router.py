import logging
from fastapi import APIRouter, HTTPException
from .create_indexes import init_indexes

# from .labels import router as labels_router
from elasticsearch import AsyncElasticsearch

elastic_router = APIRouter()

from .request import (
    create_document,
    update_document,
    get_document,
    get_document_by_id,
    get_index,
    delete_document,
    search_documents,
    # complex_query,
)


es = AsyncElasticsearch(hosts=["http://elasticsearch:9200"])
log = logging.getLogger(__name__)


def get_es_client():
    return es


@elastic_router.on_event("startup")
async def init():
    elastic_router.app.state.es = es
    # initialize elastic indexes if they aren't already
    await init_indexes(es)
    log.info("Elasticsearch router started")


@elastic_router.on_event("shutdown")
async def elastic_router_shutdown():
    await es.close()


@elastic_router.post("/{index}")
async def create_document_endpoint(index: str, document_id: str, document: dict):
    """
    Creates a new document in Elasticsearch
    """
    _document_id = await create_document(index, document_id, document, es)
    return {"document_id": _document_id}


@elastic_router.put("/{index}/{document_id}")
async def update_document_endpoint(index: str, document_id: str, document: dict):
    """
    Updates an existing document in Elasticsearch
    """
    _document_id = await update_document(index, document_id, document, es)
    return {"document_id": _document_id}


@elastic_router.get("/")
async def test_indexing():
    # for testing purposes only
    # TODO: delete this
    await init_indexes(es)
    return {"message": "success"}


@elastic_router.get("/{index}/{document_id}")
async def get_document_endpoint(index: str, document_id: str):
    """
    Retrieves a document from Elasticsearch by ID
    """
    document = await get_document(index, document_id, es)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@elastic_router.delete("/{index}/{document_id}")
async def delete_document_endpoint(index: str, document_id: str):
    """
    Deletes a document from Elasticsearch by ID
    """
    result = await delete_document(index, document_id, es)
    return {"result": result}


@elastic_router.get("/{index}")
async def search_documents_endpoint(index: str, query: str = None):
    """
    Searches for documents in Elasticsearch
    """
    if query is not None:
        documents = await search_documents(index, query, es)
    else:
        documents = await get_index(index, es)

    return documents


# @elastic_router.get("/complex/{index}")
# async def complex_search_documents_endpoint(index: str, query: str):
#     """
#     Searches for documents in Elasticsearch
#     """
#     documents = await complex_query(index, query, es)
#     return documents
