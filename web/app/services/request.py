import httpx

# import asyncio
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
import sys

sys.path.append("..")
from ..schema.messages.outbound import DeIdentRequest, _Request, _PostRequest
from ..schema.messages.inbound import _Response

# from ..services.utils import cast_to_class


async def make_request(req: _Request, res_cls: _Response) -> _Response:
    if req.method == "POST":
        res = await make_post_json_req(req, res_cls)

        return res


# TODO: use response objects
async def make_post_json_req(req: _PostRequest, res_cls: _Response):
    # response = httpx.post("http://ai-service:8081/deident", json=req)
    async with httpx.AsyncClient() as client:
        res = await client.post(req.url, json=jsonable_encoder(req))
    res_data = res.json()
    # TODO: handle all of this in the class
    _res = res_cls(
        data=res_data["data"],
        req_id=res_data["req_id"],
        time_start=res_data["time_start"],
    )
    return _res


# TODO: implement for processing multiple documents on different servers
# async def post_json(requests):
#     async with httpx.AsyncClient() as client:
#         # tasks = [make_post_json_req(client, req) for i in range(len(requests))]
#         result = await asyncio.gather(*tasks)
#         return result
