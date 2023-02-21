from fastapi import APIRouter, HTTPException
from elasticsearch import AsyncElasticsearch
from uuid import uuid4

router = APIRouter()

es = AsyncElasticsearch()


async def create_label(label):
    """
    Creates a new label in ElasticSearch
    """
    label["uuid"] = str(uuid4())
    await es.index(index="labels", id=label["uuid"], body=label)


async def update_label(uuid, label):
    """
    Updates an existing label in ElasticSearch
    """
    res = await es.update(index="labels", id=uuid, body={"doc": label})
    return res["_source"]


async def create_labels(labels):
    """
    Creates multiple labels in ElasticSearch
    """
    for label in labels:
        label["uuid"] = str(uuid4())
    await es.bulk(
        index="labels",
        body=[{"index": {"_id": label["uuid"]}} for label in labels] + labels,
    )


async def get_label(uuid):
    """
    Retrieves a label from ElasticSearch by UUID
    """
    res = await es.get(index="labels", id=uuid)
    return res["_source"]


async def search_labels(query):
    """
    Searches for labels in ElasticSearch
    """
    body = {"query": {"match": query}}
    res = await es.search(index="labels", body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]


@router.post("/labels/data/create")
async def create_label_endpoint(label: dict):
    """
    Creates a new label
    """
    await create_label(label)
    return {"message": "Label created successfully"}


@router.put("/labels/data/update")
async def update_label_endpoint(uuid: str, label: dict):
    """
    Updates an existing label
    """
    updated_label = await update_label(uuid, label)
    return updated_label


@router.post("/labels/data/create/bulk")
async def create_labels_endpoint(labels: list):
    """
    Creates multiple labels
    """
    await create_labels(labels)
    return {"message": "Labels created successfully"}


@router.get("/labels/data/read/{uuid}")
async def get_label_endpoint(uuid: str):
    """
    Retrieves a label by UUID
    """
    label = await get_label(uuid)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label


@router.get("/labels/data/search/{query}")
async def search_labels_endpoint(query: str):
    """
    Searches for labels
    """
    labels = await search_labels(query)
    return labels
