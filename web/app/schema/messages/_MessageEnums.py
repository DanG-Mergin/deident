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
    deID = "deID"


class UI_Entity(str, Enum):
    doc = "doc"
    label = "label"
    substitution = "substitution"


# TODO: rethink this whole idea
class UI_EntityType(str, Enum):
    ner = "ner"
    deID = "deID"
    dictionary = "dictionary"
