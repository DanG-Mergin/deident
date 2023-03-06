import logging
from fastapi import APIRouter, HTTPException, Request
from .create_indexes import init_indexes
from pydantic import BaseModel, ValidationError
from typing import Type

# from .schema.Label import Label
from ...schema.base.entities._Label import _Label as Label

# from .schema.Doc import Doc
from ...schema.base.entities._Doc import _Doc as Doc
from ...schema.base.messages._ElasticRequest import _ElasticRequest

from ...schema.base.messages._Response import _Response


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


# Dictionary that maps model names to Pydantic classes
MODEL_MAP = {"label": Label, "doc": Doc}


def get_model(model_name: str) -> Type[BaseModel]:
    try:
        return MODEL_MAP[model_name]
    except KeyError:
        raise ValueError(f"Unknown model name: {model_name}")


@elastic_router.on_event("startup")
async def init():
    elastic_router.app.state.es = es
    await init_indexes(es)

    # initialize elastic indexes if they aren't already

    log.info("Elasticsearch router started")
    print("Elasticsearch router started")


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
async def update_document_endpoint(index: str, document_id: str, req: Request):
    """
    Updates an existing document in Elasticsearch
    """
    req_data = await req.json()
    _req = _ElasticRequest.parse_obj(req_data)

    cls = get_model(index)
    try:
        document = cls(**_req.data.items[0])
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # if not await get_document(index, document_id, es):
    #     _document_id = await create_document(index, document_id, document, es)
    #     # raise HTTPException(status_code=404, detail="Document not found")
    # else:
    _document_id = await update_document(index, document_id, document.dict(), es)
    # TODO: Delete this test
    _test_doc = await get_document(index, document_id, es)
    # _res = _Response(data={"item_ids": [document_id]})
    _res = _Response.parse_obj(_req.dict())
    return _res


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
    try:
        if query is not None:
            documents = await search_documents(index, query, es)
        else:
            documents = await get_index(index, es)

        cls = get_model(index)
        items = [cls(**doc["_source"]) for doc in documents]
        res = _Response(data={"items": items})

        return res
    except Exception as e:
        print(str(e))
        return _Response(error=e)


# @elastic_router.get("/complex/{index}")
# async def complex_search_documents_endpoint(index: str, query: str):
#     """
#     Searches for documents in Elasticsearch
#     """
#     documents = await complex_query(index, query, es)
#     return documents
