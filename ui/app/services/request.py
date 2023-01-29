import httpx

# import asyncio
from pydantic import ValidationError
import sys

sys.path.append("..")
from ..schema.outbound import DeIdentRequest, _Request, _PostRequest
from ..schema.inbound import _Response


# TODO: add config to env


# TODO: clean this unholy mess up hahahaha
async def make_request(req: _Request) -> _Response:
    if req.req_type == "post":
        res = await make_post_json_req(req)

        return res
    # elif req.req_type == 'get':
    #     async with httpx.AsyncClient() as client:
    #         try:
    #             res = await client.get("http://ai-service:8081/")
    #         except httpx.RequestError as exc:
    #             print(exc)
    #         # TODO: handle error and return properly
    #         return res


# TODO: use response objects
async def make_post_json_req(req):
    response = httpx.post("http://ai-service:8081/deident", data=req.data)
    # response = await httpx.post(req.url, json=req.data)
    print(response)
    print("hi")
    # async with httpx.AsyncClient() as client:
    #     res = await client.post(req.url, json=req.data)
    #     try:
    #         _res = _Response(res)
    #         return _res
    #     except ValidationError as e:
    #         print(e)  # TODO: log this and handle completely


# TODO: implement for processing multiple documents on different servers
# async def post_json(requests):
#     async with httpx.AsyncClient() as client:
#         # tasks = [make_post_json_req(client, req) for i in range(len(requests))]
#         result = await asyncio.gather(*tasks)
#         return result
