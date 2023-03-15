from ..services import request
from ..services.utils import cast_to_class

from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Observable import _Observable

from ..schema.ui.Annotation import Annotation
from ..schema.base.entities._Revisions import _Revisions
from ..schema.data._ElasticRequest import _ElasticRequest, _ElasticsearchQuery


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

    # TODO: just testing queries
    blep = await get_annotations(_req)
    return res


# retrieves latest annotations from data server
# TODO: currently just testing queries
async def get_annotations(req: _Observable) -> _Response:
    _query = {
        "query": {"range": {"timestamp": {"gte": "now-1y", "lte": "now"}}},
        "sort": {"timestamp": {"order": "asc"}},
        "from": 0,
        "size": 10,
    }
    req.query = _query
    req.msg_action = "search"
    req.msg_entity = "annotation"
    _req = cast_to_class(
        req,
        _ElasticRequest,
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res


async def search(req: _Observable) -> _Response:
    if req.query is None:
        _query = {
            "query": {"match_all": {}},
            "from": 0,
            "size": 10,
        }

    _req = cast_to_class(
        req,
        _ElasticRequest,
        query=_query,
    )
    res = await request.make_request(_req, res_cls=_Response)
    return res
