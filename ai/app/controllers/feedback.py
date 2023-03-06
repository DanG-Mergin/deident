# For handling user feedback

from typing import List
from ..services import request

# from ..schema.messages.inbound.DeIDRequest import DeIDRequest
# from ..schema.messages.outbound.DeIDResponse import DeIDResponse
from ..schema.messages.outbound.ElasticRequest import ElasticRequest

# from ..schema.messages.inbound.ElasticResponse import ElasticResponse
from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Request import _Request


async def update_deID(req: _Request) -> _Response:

    # first save the feedback to the database in case of error/rollback/etc
    try:
        _req = ElasticRequest(**req.dict())
        _res = await request.make_request(_req, res_cls=_Response)
        # res = DeIDResponse(**_res.dict())

        return _res
        # TODO: logic to utilize deidentification updates from the UI
    except Exception as e:
        print(str(e))
