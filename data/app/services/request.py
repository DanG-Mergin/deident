import httpx

# import asyncio
# from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
import sys

sys.path.append("..")
from ..schema.outbound import _Request, _PostRequest
from ..schema.inbound import _Response


async def make_request(req: _Request, res_cls: _Response) -> _Response:
    if req.method == "POST":
        res = await make_post_json_req(req, res_cls)

        return res


async def make_post_json_req(req: _PostRequest, res_cls: _Response):
    async with httpx.AsyncClient() as client:
        res = await client.post(req.url, json=jsonable_encoder(req))

    res_data = res.json()

    _res = res_cls(
        data=res_data["data"],
        req_id=res_data["req_id"],
        time_start=res_data["time_start"],
    )
    return _res
