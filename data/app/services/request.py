import httpx

# import asyncio
# from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
import sys

sys.path.append("..")
from ..schema.outbound import _Request, _PostRequest
from ..schema.inbound import _Response

client = httpx.AsyncClient()


async def make_request(req: _Request, res_cls: _Response) -> _Response:
    if req.method == "POST":
        # res = await make_post_json_req(req, res_cls)
        res = await client.post(req.url, json=jsonable_encoder(req))
    elif req.method == "GET":
        # url = req.url
        res = await client.get(req.url)
        # res = await make_get_req(req, res_cls)
    elif req.method == "PUT":
        res = await client.put(req.url, json=jsonable_encoder(req))
        # res = await make_put_req(req, res_cls)
    elif req.method == "DELETE":
        res = await client.delete(req.url, json=jsonable_encoder(req))
        # res = await make_delete_req(req, res_cls)
    else:
        raise ValueError(f"Unsupported method: {req.method}")

    res_data = res.json()
    # TODO: handle all of this in the class
    _res = res_cls(
        data=res_data["data"],
        uuid=req.uuid,
        # orig_id=req.orig_id,
    )
    return _res
