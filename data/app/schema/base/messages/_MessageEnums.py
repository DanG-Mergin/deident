from enum import Enum, IntEnum


class MsgAction(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"
    # index = "index"
    search = "search"


class MsgStatus(str, Enum):
    success = "success"
    error = "error"
    loading = "loading"
    idle = "idle"
    pending = "pending"


class MsgType(str, Enum):
    data = "data"
    state = "state"
    index = "index"


class MsgTask(str, Enum):
    deid = "deID"
    drug = "drug"


class MsgEntity(str, Enum):
    annotation = "annotation"
    corpus = "corpus"
    doc = "doc"
    label = "label"
    entity = "entity"
    token = "token"
    substitution = "substitution"


# TODO: rethink this whole idea
class MsgEntity_Type(str, Enum):
    ner = "ner"
    deid = "deID"
    drug = "drug"
    dictionary = "dictionary"


# Maps msg_action in observable requests to the corresponding Elasticsearch method
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


# maps MsgEntity to the corresponding Elasticsearch index
class ElasticIndexes(str, Enum):
    labels = "label"
    label = "label"
    substitutions = "substitution"
    substitution = "substitution"
    doc = "doc"
    docs = "doc"
    annotation = "annotation"
    annotations = "annotation"
    corpus = "corpus"


# maps MsgTask to the corresponding Elasticsearch type
class ElasticTasks(str, Enum):
    deid = "deID"
    drug = "drug"
