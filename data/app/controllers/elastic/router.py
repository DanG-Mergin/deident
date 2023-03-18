import logging
from fastapi import APIRouter, HTTPException, Request
from ...emitter import emitter

from ...services.elastic.create_indexes import init_indexes
from pydantic import BaseModel, ValidationError
from typing import Type

# from .schema.Label import Label
from ...schema.base.entities._Label import _Label as Label

# from .schema.Doc import Doc
from ...schema.base.entities._Doc import _Doc as Doc
from ...schema.base.entities._Annotation import _Annotation as Annotation
from ...schema.base.messages._ElasticRequest import _ElasticRequest
from ...schema.base.entities._Corpus import _Corpus as Corpus

from ...schema.base.messages._Response import _Response
from ...schema.base.messages._MessageEnums import MsgAction

# from .labels import router as labels_router
from elasticsearch import AsyncElasticsearch

elastic_router = APIRouter()

from ...services.elastic.request import (
    create_document,
    update_document,
    get_document,
    get_document_by_id,
    get_index,
    delete_document,
    search_documents,
    # complex_query,
)
from ...services.elastic.dependencies import get_elasticsearch_client

# from . import CorpusCtrl.CorpusCtrl as corpus_c, DocCtrl as doc_c, _RequestCtrl as request_c
from .CorpusCtrl import CorpusCtrl as corpus_c
from .DocCtrl import DocCtrl as doc_c
from ._RequestCtrl import _RequestCtrl as request_c

_es = get_elasticsearch_client()

# es = AsyncElasticsearch(hosts=["http://elasticsearch:9200"])
log = logging.getLogger(__name__)


# Dictionary that maps model names to Pydantic classes
MODEL_MAP = {
    "annotation": Annotation,
    "corpus": Corpus,
    "doc": Doc,
    "label": Label,
}
CTRL_MAP = {"doc": doc_c, "corpus": corpus_c}


def get_model(model_name: str) -> Type[BaseModel]:
    try:
        return MODEL_MAP[model_name]
    except KeyError:
        raise ValueError(f"Unknown model name: {model_name}")


def get_controller(index: str):
    if index in CTRL_MAP:
        return CTRL_MAP[index]
    return request_c


# @elastic_router.on_event("startup")
async def init():

    # initialize elastic indexes if they aren't already
    await init_indexes()
    log.info("Elasticsearch router started")
    print("Elasticsearch router started")


@elastic_router.on_event("shutdown")
async def elastic_router_shutdown():
    await _es.close()


# for testing only
@elastic_router.get("/search/{index}")
async def test_search(index: str):
    query = {
        "query": {"range": {"timestamp": {"gte": "now-1y", "lte": "now"}}},
        "sort": {"timestamp": {"order": "asc"}},
        "from": 0,
        "size": 10,
    }
    res = await search_documents(index, query)
    return res


@elastic_router.post("/search/{index}")
async def search_documents_endpoint(index: str, req: Request):
    req_data = await req.json()
    _req = _ElasticRequest.parse_obj(req_data)

    # cls = get_model(index)
    # try:
    #     document = cls(**_req.data.items[0].dict())
    # except ValidationError as e:
    #     raise HTTPException(status_code=422, detail=str(e))

    _res = _Response.parse_obj(_req.dict())
    _es_res = await search_documents(index, _req.query)
    _res.data = {"items": _es_res}
    _res.msg_status = "success"

    # await emitter.publish(_res)
    return _res


@elastic_router.post("/{index}/{document_id}")
@elastic_router.post("/{index}")
# async def create_document_endpoint(index: str, document_id: str, document: dict):
async def create_document_endpoint(index: str, req: Request):

    req_data = await req.json()
    _req = _ElasticRequest.parse_obj(req_data)
    document_id = _req.data.item_ids[0]

    cls = get_model(index)
    try:
        document = cls(**_req.data.items[0].dict())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    controller = get_controller(index)

    # _document_id = await controller.create_document(
    #     index, _req.data.item_ids[0], document.dict()
    # )
    _document_id = await controller.create_document(
        index, _req.data.item_ids[0], document
    )

    # TODO: consolidate this with update document endpoint

    _res = _Response.parse_obj(_req.dict())
    _res.data = {"item_ids": [document_id]}
    _res.msg_status = "success"

    await emitter.publish(_res)
    return _res


@elastic_router.put("/{index}/{document_id}")
async def update_document_endpoint(index: str, document_id: str, req: Request):
    """
    Updates an existing document in Elasticsearch
    """
    req_data = await req.json()
    _req = _ElasticRequest.parse_obj(req_data)

    cls = get_model(index)
    try:
        document = cls(**_req.data.items[0].dict())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    controller = get_controller(index)

    # if not await get_document(index, document_id, es):
    #     _document_id = await create_document(index, document_id, document, es)
    #     # raise HTTPException(status_code=404, detail="Document not found")
    # else:
    _document_id = await controller.update_document(index, document_id, document)

    _res = _Response.parse_obj(_req.dict())
    _res.data = {"item_ids": [document_id]}
    _res.msg_status = "success"

    await emitter.publish(_res)
    return _res


@elastic_router.get("/")
async def test_indexing():
    # for testing purposes only
    # TODO: delete this
    await init_indexes()
    return {"message": "success"}


@elastic_router.get("/{index}/{document_id}")
async def get_document_endpoint(index: str, document_id: str):
    """
    Retrieves a document from Elasticsearch by ID
    """
    document = await get_document(index, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    cls = get_model(index)
    document = cls(**document)
    res = _Response(
        data={"items": [document]},
        msg_status="success",
        msg_action="read",
        msg_entity=index,
    )
    return res


@elastic_router.delete("/{index}/{document_id}")
async def delete_document_endpoint(index: str, document_id: str):
    """
    Deletes a document from Elasticsearch by ID
    """
    controller = get_controller(index)
    result = await controller.delete_document(index, document_id)
    return {"result": result}


@elastic_router.get("/{index}")
async def search_documents_endpoint(index: str, query: str = None):
    """
    Searches for documents in Elasticsearch
    """
    try:
        if query is not None:
            documents = await search_documents(index, query)
        else:
            documents = await get_index(index)

        cls = get_model(index)
        items = [cls(**doc["_source"]) for doc in documents]
        res = _Response(
            data={"items": items},
            msg_status="success",
            msg_action="search",
            msg_entity=index,
        )

        return res
    except Exception as e:
        print(str(e))
        return _Response(error=e)


# @elastic_router.get("/complex/{index}")
# async def complex_search_documents_endpoint(index: str, query: str):
#     """
#     Searches for documents in Elasticsearch
#     """
#     documents = await complex_query(index, query)
#     return documents
