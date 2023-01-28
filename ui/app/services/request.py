import httpx
# import asyncio
from pydantic import ValidationError
import sys
sys.path.append("..")
from ..schema.outbound import DeIdentRequest, _Request, _PostRequest
from ..schema.inbound import _Response


# TODO: add config to env
# config = {
#     "ENV": "DEV",
#     "DEV": {
#         "paths": {
#             "data": "http://localhost:8082",
#             "deident": "http://localhost:8083",
#             "extraction": "http://localhost:8083"
#         }
#     }
# }

# TODO: clean this unholy mess up hahahaha
async def make_request(req: _Request)-> _Response:
    # if req.host_name is "ai" and req.meta_type is "deident":
    #     _req = DeIdentRequest(req)
    if isinstance(req, type(_PostRequest)):
        res = await make_post_json_req(req)
        return res

# TODO: use response objects
async def make_post_json_req(req):
    async with httpx.AsyncClient() as client:
        res = await client.post(req.url, data=req.data)
        try: 
            _res = _Response(res)
        except ValidationError as e:
            print(e) #TODO: log this and handle completely
        return _res


# TODO: implement for processing multiple documents on different servers
# async def post_json(requests):
#     async with httpx.AsyncClient() as client:
#         # tasks = [make_post_json_req(client, req) for i in range(len(requests))]
#         result = await asyncio.gather(*tasks)
#         return result
