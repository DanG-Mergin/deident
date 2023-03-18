import asyncio
from .dependencies import get_elasticsearch_client

_es = get_elasticsearch_client()
# from .schema._ElasticRequest import ElasticsearchQuery


async def create_document(index, document_id, document, es=_es):
    """
    Creates a new document in Elasticsearch
    """
    # res = await es.index(index=index, id=document_id, body={"doc": document})
    res = await es.index(index=index, id=document_id, body=document)
    return res["_id"]


async def update_document(index, document_id, document, es=_es):
    """
    Updates an existing document in Elasticsearch with only the fields present in the 'document' object
    """
    # Prepare the script to update only the fields present in the 'document' object
    script_lines = []
    for field in document:
        script_lines.append(f"ctx._source.{field} = params.{field};")

    script = " ".join(script_lines)

    # Update the document in Elasticsearch using the prepared script
    res = await es.update(
        index=index,
        id=document_id,
        body={
            "script": {
                "source": script,
                "lang": "painless",
                "params": document,
            },
            # "upsert": document, # this would create the document if it doesn't exist, but would effectively sidestep required fields
        },
    )
    return res["_id"]


async def get_index(index, es=_es):
    """
    Retrieves an index from Elasticsearch
    """
    res = await es.search(index=index, body={"query": {"match_all": {}}, "size": 1000})
    # return res["_source"]
    return res["hits"]["hits"]


async def get_document(index, document_id, es=_es):
    """
    Retrieves a document from Elasticsearch by ID
    """
    res = await es.get(index=index, id=document_id)
    return res["_source"]


async def get_document_by_id(index, document_id, es=_es):
    """
    Retrieves a document from Elasticsearch by ID
    """
    res = await es.get(index=index, id=document_id)
    return res["_source"]


async def delete_document(index, document_id, es=_es):
    """
    Deletes a document from Elasticsearch by ID
    """
    res = await es.delete(index=index, id=document_id)
    return res["result"]


async def search_documents(index, query, es=_es):
    """
    Searches for documents in Elasticsearch
    """
    # _query = query.dict()

    res = await es.search(index=index, body=query)
    return [hit["_source"] for hit in res["hits"]["hits"]]


async def bulk_create_documents(index, documents, es=_es):
    """
    Creates multiple documents in Elasticsearch using the bulk API
    """
    tasks = [
        es.index(index=index, id=document["uuid"], body=document)
        for document in documents
    ]
    res = await asyncio.gather(*tasks)
    return res


async def bulk_get_documents(index, document_ids, es=_es):
    """
    Retrieves multiple documents from Elasticsearch by ID using the mget API
    """
    mget_body = {"ids": document_ids}
    res = await es.mget(index=index, body=mget_body)
    return [hit["_source"] for hit in res["docs"]]


async def bulk_update_documents(index, documents, es=_es):
    """
    Updates multiple documents in Elasticsearch using the update API
    """
    tasks = [
        es.update(index=index, id=document["uuid"], body={"document": document})
        for document in documents
    ]
    return await asyncio.gather(*tasks)


async def bulk_delete_documents(index, document_ids, es=_es):
    """
    Deletes multiple documents from Elasticsearch by ID using the delete API
    """
    tasks = [es.delete(index=index, id=document_id) for document_id in document_ids]
    return await asyncio.gather(*tasks)


# async def complex_query(index: str, query: ElasticsearchQuery, es=_es):
#     # Construct Elasticsearch query
#     body = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {
#                         "multi_match": {
#                             "query": query.query,
#                             "type": "cross_fields",
#                             "fields": ["*"],
#                             "operator": "and",
#                         }
#                     }
#                 ]
#             }
#         },
#         "sort": [{"_score": {"order": "desc"}}],
#         "from": (query.page_number - 1) * query.page_size,
#         "size": query.page_size,
#     }

#     if query.sort_by:
#         body["sort"] = [
#             {"_score": {"order": "desc"}},
#             {query.sort_by: {"order": "asc"}},
#         ]

#     # Apply filters
#     filters = query.filters
#     if filters:
#         filter_list = [f.dict() for f in filters]
#         body["query"]["bool"].update({"filter": filter_list})

#     # Execute query
#     results = await es.search(index="my_index", body=body)

#     return results
