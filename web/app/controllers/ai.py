from ..services import request
from ..services.utils import cast_to_class
from ..schema.ai.DeIDRequest import DeIDRequest

# from ..schema.ai.DeIDResponse import DeIDResponse
from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Observable import _Observable


async def deID(req: _Observable) -> _Response:
    _req = cast_to_class(req, DeIDRequest)
    res = await request.make_request(_req, res_cls=_Response)

    return res


# Deprecated
# async def update_deID(req: _Observable) -> _Response:
#     # TODO: push new annotations up to data, have ai listen for changes
#     # and do something if criteria are met
#     _req = cast_to_class(req, DeIDRequest)
#     res = await request.make_request(_req, res_cls=_Response)

#     return res
