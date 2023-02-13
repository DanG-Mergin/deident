# utils.py is for SHARED abstract work
from pydantic import BaseModel


def cast_to_class(obj1: BaseModel, cls: BaseModel, **kwargs):
    if isinstance(obj1, BaseModel):
        attr = attr = {k: v for k, v in obj1.__dict__.items()}
    else:
        kwargs = {**kwargs, **obj1}
        return cls(**kwargs)
    return cls(**kwargs, **attr)
