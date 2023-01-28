
from pydantic import ValidationError
import sys
sys.path.append("..")
from ..schema.InternalMsg import InternalMsg
from ..schema.outbound.DeIdentRequest import DeIdentRequest
from .request import make_request

# TODO: add object casting decorator function
async def deident(req: InternalMsg) -> InternalMsg:
    # req['host_name'] = 'ai'
    # req['service_name'] = 'deident'
    try: 
        # d_req = DeIdentRequest.from_msg(req, host_name='ai')
        d_req = DeIdentRequest.from_obj(req, host_name='ai')
        res = await make_request(d_req)
    except ValidationError as e:
        print(e) #TODO: log this and handle completely

    return res
