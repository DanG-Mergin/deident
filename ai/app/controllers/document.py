from typing import List
from ..services import spacy as spacy_s
from ..services.utils import cast_to_class
from ..services import request
from ..schema.base.messages._ElasticRequest import _ElasticRequest
from ..schema.base.messages._Request import _Request
from ..schema.base.messages._Response import _Response

# takes a previously unannotated text, backs it up in the database, and returns the annotated text
async def deID(req: _Request) -> _Response:
    # First we need to save the unannotated text to the database
    _res = await save_document(req)

    if _res:
        # If the save was successful we can annotate the text
        annotations = await spacy_s.deID(req.data.items)

        res = cast_to_class(req, _Response, data={"items": annotations}, uuid=req.uuid)
    return res


async def save_document(req: _Request) -> _Response:
    _res = None
    try:
        _req = _ElasticRequest(**req.dict())
        _res = await request.make_request(_req, res_cls=_Response)

    except Exception as e:
        print(str(e))
        return e
        # TODO: robust error handling
    return _res


# For handling user feedback
async def update_deID(req: _Request) -> _Response:

    # first save the feedback to the database in case of error/rollback/etc
    _res = await save_document(req)
    return _res
    # try:
    #     _req = _ElasticRequest(**req.dict())
    #     _res = await request.make_request(_req, res_cls=_Response)

    #     return _res
    #     # TODO: logic to utilize deidentification updates from the UI
    # except Exception as e:
    #     print(str(e))
