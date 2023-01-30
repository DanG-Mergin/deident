# utils.py is for SHARED abstract work
from pydantic import BaseModel


def cast_to_class(obj1: BaseModel, cls: BaseModel, **kwargs):
    attr = attr = {k: v for k, v in obj1.__dict__.items()}
    if kwargs:
        return cls(**attr, **kwargs)
    return cls(**attr)
