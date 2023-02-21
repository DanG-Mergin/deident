from enum import Enum, IntEnum


class O_Action(str, Enum):
    create: "create"
    read: "read"
    update: "update"
    delete: "delete"
    index: "index"
    search: "search"


class O_Status(str, Enum):
    success: "success"
    error: "error"
    refetching: "refetching"
    isFetchingMore: "isFetchingMore"
    isUpdating: "isUpdating"


class O_Type(str, Enum):
    data: "data"
    state: "state"
    index: "index"


class UI_Entity(str, Enum):
    deident: "deident"
