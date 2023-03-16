from elasticsearch import AsyncElasticsearch

_es_instance = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    global _es_instance
    if _es_instance is None:
        # TODO: move path to config file
        _es_instance = AsyncElasticsearch(hosts=["http://elasticsearch:9200"])
    return _es_instance
