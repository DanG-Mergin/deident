from ..services import request
from ..schema.data._ElasticRequest import _ElasticRequest

from ..schema.base.messages._Response import _Response
from ..schema.ui.Observable import _Observable as Observable


async def elastic(req: Observable) -> _Response:
    # res = await ai_s.deID(req)
    _req = _ElasticRequest(**req.dict())
    res = await request.make_request(_req, res_cls=_Response)

    return res
