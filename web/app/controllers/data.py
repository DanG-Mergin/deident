from ..services import request
from ..services.utils import cast_to_class

from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Observable import _Observable

from ..schema.ui.Annotation import Annotation
from ..schema.base.entities._Revisions import _Revisions
from ..schema.data._ElasticRequest import _ElasticRequest


async def create_doc(req: _Observable) -> _Response:
    _req = cast_to_class(
        req,
        _ElasticRequest,
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res


async def read(req: _Observable) -> _Response:
    _req = cast_to_class(
        req,
        _ElasticRequest,
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res


# TODO: web should be saving to the data server and being notified when
# the ai server has finished processing
async def update_deID(req: _Observable) -> _Response:
    # anno = _Revisions(**req.data.items[1])
    anno = _Revisions(**req.data.items[0])
    _anno = cast_to_class(anno, Annotation)
    _req = cast_to_class(
        req,
        _ElasticRequest,
        data={"item_ids": [_anno.uuid], "items": [_anno]},
        msg_entity="annotation",
        msg_action="create",
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res


# retrieves latest annotations from data server
async def get_annotations(req: _Observable) -> _Response:
    _req = cast_to_class(
        req,
        _ElasticRequest,
        msg_entity="annotation",
        msg_action="read",
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res


async def search(req: _Observable) -> _Response:
    # TODO: for now it just returns the first 10 results of an index
    _req = cast_to_class(
        req,
        _ElasticRequest,
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res
