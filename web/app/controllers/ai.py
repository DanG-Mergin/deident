from ..services import request
from ..schema.messages.outbound.DeIDRequest import DeIDRequest
from ..schema.messages.inbound.DeIDResponse import DeIDResponse


async def deID(req: DeIDRequest) -> DeIDResponse:
    res = await request.make_request(req, res_cls=DeIDResponse)

    return res


async def update_deID(req: DeIDRequest) -> DeIDResponse:
    res = await request.make_request(req, res_cls=DeIDResponse)

    return res
