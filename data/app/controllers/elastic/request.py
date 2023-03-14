import asyncio

# from .schema._ElasticRequest import ElasticsearchQuery


async def create_document(index, document_id, document, es):
    """
    Creates a new document in Elasticsearch
    """
    # res = await es.index(index=index, id=document_id, body={"doc": document})
    res = await es.index(index=index, id=document_id, body=document)
    return res["_id"]


async def update_document(index, document_id, document, es):
    """
    Updates an existing document in Elasticsearch
    """
    res = await es.update(
        index=index, id=document_id, body={"doc": document, "doc_as_upsert": True}
    )
    return res["_id"]


async def get_index(index, es):
    """
    Retrieves an index from Elasticsearch
    """
    res = await es.search(index=index, body={"query": {"match_all": {}}, "size": 1000})
    # return res["_source"]
    return res["hits"]["hits"]


async def get_document(index, document_id, es):
    """
    Retrieves a document from Elasticsearch by ID
    """
    res = await es.get(index=index, id=document_id)
    return res["_source"]


async def get_document_by_id(index, document_id, es):
    """
    Retrieves a document from Elasticsearch by ID
    """
    res = await es.get(index=index, id=document_id)
    return res["_source"]


async def delete_document(index, document_id, es):
    """
    Deletes a document from Elasticsearch by ID
    """
    res = await es.delete(index=index, id=document_id)
    return res["result"]


async def search_documents(index, query, es):
    """
    Searches for documents in Elasticsearch
    """
    body = {"query": {"match": query}}
    res = await es.search(index=index, body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]


async def bulk_create_documents(index, documents, es):
    """
    Creates multiple documents in Elasticsearch using the bulk API
    """
    tasks = [
        es.index(index=index, id=document["uuid"], body=document)
        for document in documents
    ]
    res = await asyncio.gather(*tasks)
    return res


async def bulk_get_documents(index, document_ids, es):
    """
    Retrieves multiple documents from Elasticsearch by ID using the mget API
    """
    mget_body = {"ids": document_ids}
    res = await es.mget(index=index, body=mget_body)
    return [hit["_source"] for hit in res["docs"]]


async def bulk_update_documents(index, documents, es):
    """
    Updates multiple documents in Elasticsearch using the update API
    """
    tasks = [
        es.update(index=index, id=document["uuid"], body={"document": document})
        for document in documents
    ]
    return await asyncio.gather(*tasks)


async def bulk_delete_documents(index, document_ids, es):
    """
    Deletes multiple documents from Elasticsearch by ID using the delete API
    """
    tasks = [es.delete(index=index, id=document_id) for document_id in document_ids]
    return await asyncio.gather(*tasks)


# async def complex_query(index: str, query: ElasticsearchQuery, es):
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
