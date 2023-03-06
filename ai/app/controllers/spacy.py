from typing import List
from ..services import spacy as spacy_s
from ..services.utils import cast_to_class

# from ..schema.messages.inbound.DeIDRequest import DeIDRequest
# from ..schema.messages.outbound.DeIDResponse import DeIDResponse
from ..schema.base.messages._Request import _Request
from ..schema.base.messages._Response import _Response


async def deID(req: _Request) -> _Response:
    annotations = await spacy_s.deID(req.data.items)
    # res = _Response(data={"items": annotations}, uuid=req.uuid)
    res = cast_to_class(req, _Response, data={"items": annotations}, uuid=req.uuid)
    return res
