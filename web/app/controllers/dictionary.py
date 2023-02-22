from ..services import request
from ..schema.messages.outbound.ElasticRequest import ElasticRequest
from ..schema.messages.inbound.ElasticResponse import ElasticResponse
from ..schema.messages.inbound._Observable import _Observable as Observable


async def elastic(req: Observable) -> ElasticResponse:
    # res = await ai_s.deID(req)
    _req = ElasticRequest(**req.dict())
    res = await request.make_request(_req, res_cls=ElasticResponse)

    return res
