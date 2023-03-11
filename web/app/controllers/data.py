from ..services import request
from ..services.utils import cast_to_class

from ..schema.base.messages._Response import _Response
from ..schema.base.messages._Observable import _Observable

from ..schema.ui.Annotation import Annotation
from ..schema.base.entities._Revisions import _Revisions
from ..schema.data._ElasticRequest import _ElasticRequest

# TODO: web should be saving to the data server and being notified when
# the ai server has finished processing
async def update_deID(req: _Observable) -> _Response:
    anno = _Revisions(**req.data.items[1])
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
