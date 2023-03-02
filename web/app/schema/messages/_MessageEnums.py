from enum import Enum, IntEnum


class O_Action(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    # index = "index"
    search = "search"


class O_Status(str, Enum):
    success = "success"
    error = "error"
    loading = "loading"
    idle = "idle"
    pending = "pending"


class O_Type(str, Enum):
    data = "data"
    state = "state"
    index = "index"


class Job_Task(str, Enum):
    deid = "deID"


class UI_Entity(str, Enum):
    doc = "doc"
    label = "label"
    substitution = "substitution"


# TODO: rethink this whole idea
class UI_EntityType(str, Enum):
    ner = "ner"
    deid = "deID"
    dictionary = "dictionary"


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
    doc = "document"
    docs = "document"


# maps Job_Task to the corresponding Elasticsearch type
class ElasticTasks(str, Enum):
    deid = "deID"
