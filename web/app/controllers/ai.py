from ..services import request
from ..schema.ai.DeIDRequest import DeIDRequest

# from ..schema.ai.DeIDResponse import DeIDResponse
from ..schema.base.messages._Response import _Response


async def deID(req: DeIDRequest) -> _Response:
    res = await request.make_request(req, res_cls=_Response)

    return res


async def update_deID(req: DeIDRequest) -> _Response:
    res = await request.make_request(req, res_cls=_Response)

    return res
