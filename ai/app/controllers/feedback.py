# For handling user feedback

from typing import List
from ..services import request

from ..schema.base.messages._ElasticRequest import _ElasticRequest


from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Request import _Request


async def update_deID(req: _Request) -> _Response:

    # first save the feedback to the database in case of error/rollback/etc
    try:
        _req = _ElasticRequest(**req.dict())
        _res = await request.make_request(_req, res_cls=_Response)

        return _res
        # TODO: logic to utilize deidentification updates from the UI
    except Exception as e:
        print(str(e))
