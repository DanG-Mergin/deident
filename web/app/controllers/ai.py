import sys

sys.path.append("..")
from ..services import request
from ..schema.messages.outbound.DeIdentRequest import DeIdentRequest
from ..schema.messages.inbound.DeIdentResponse import DeIdentResponse


async def deident(req: DeIdentRequest) -> DeIdentResponse:
    # res = await ai_s.deident(req)
    res = await request.make_request(req, res_cls=DeIdentResponse)

    return res
