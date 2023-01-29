
from pydantic import ValidationError
import sys
sys.path.append("..")
from ..schema.InternalMsg import InternalMsg
from ..schema.outbound.DeIdentRequest import DeIdentRequest
from .request import make_request
from .utils import cast_to_class

async def deident(req: InternalMsg) -> InternalMsg:
    try: 
        d_req = cast_to_class(req, DeIdentRequest, host_name='ai')
        res = await make_request(d_req)
    except ValidationError as e:
        print(e) #TODO: log this and handle completely

    return res
