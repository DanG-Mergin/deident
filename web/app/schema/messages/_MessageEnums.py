
from enum import Enum, IntEnum

class Action(Enum):
    create: 'create'
    read: 'read'
    update: 'update'
    delete: 'delete'

class Status(Enum):
    success: 'success'
    failure: 'failure'