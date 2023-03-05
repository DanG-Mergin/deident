from enum import Enum

# Maps o_action in observable requests to the corresponding Elasticsearch method
class ElasticMethod(str, Enum):
    search = "GET"
    get = "GET"
    read = "GET"
    delete = "DELETE"
    update = "PUT"
    put = "PUT"
    bulk = "POST"
    post = "POST"
    create = "POST"


# maps UI_Entity to the corresponding Elasticsearch index
class ElasticIndexes(str, Enum):
    labels = "label"
    label = "label"
    substitutions = "substitution"
    substitution = "substitution"
    docs = "document"
    doc = "document"


# maps Job_Task to the corresponding Elasticsearch type
class ElasticTasks(str, Enum):
    deid = "deID"
