# utils.py is for SHARED abstract work
from pydantic import BaseModel


def cast_to_class(obj1: BaseModel, cls: BaseModel, **kwargs):
    if isinstance(obj1, BaseModel):
        attr = attr = {k: v for k, v in obj1.__dict__.items() if k not in kwargs}
    else:
        kwargs = {**kwargs, **obj1}
        return cls(**kwargs)
    return cls(**kwargs, **attr)


def is_property_specified(input_dict, valid_keys):
    for key in valid_keys:
        if key in input_dict:
            return True  # At least one valid key is present, so return without raising an exception
    # If none of the valid keys are present, raise an exception
    raise ValueError(
        f"At least one of the following keys must be specified: {valid_keys}"
    )


def get_matching_objects(**kwargs):
    # won't need this once we have a db most likely
    # doesn't handle nested objects

    # index = [
    #     {
    #         "category": "NAME",
    #         "subCategory": "PATIENT",
    #         "types": ["ner"],
    #         "tasks": ["deID"],
    #         "kb_id": '1',
    #         "uuid": "7cf57950-0feb-41cc-ab60-d270e1a3f6e9",
    #         "substitutionId": "2545a46b-e5f7-4d77-9d13-d137e875adc2"
    #     }
    #     # ... list of objects ...
    # ]

    if not kwargs:
        raise ValueError("At least one keyword argument must be specified")

    for key, value in kwargs.items():
        index = [obj for obj in index if (key in obj) and (value in obj.get(key, []))]

    return index
