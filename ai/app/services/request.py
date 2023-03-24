import httpx

# import asyncio
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from .utils import cast_to_class

# from ..schema.messages.outbound import _Request
from ..schema.base.messages._Request import _Request

# from ..schema.messages.inbound import _Response
from ..schema.base.messages._Response import _Response

client = httpx.AsyncClient()


async def make_request(
    req: _Request, res_cls: _Response, timeout: int = 5
) -> _Response:
    if req.method == "POST":
        res = await client.post(req.url, json=jsonable_encoder(req), timeout=timeout)
    elif req.method == "GET":
        res = await client.get(req.url, timeout=timeout)
    elif req.method == "PUT":
        res = await client.put(req.url, json=jsonable_encoder(req), timeout=timeout)
    elif req.method == "DELETE":
        res = await client.delete(req.url, json=jsonable_encoder(req), timeout=timeout)
    else:
        raise ValueError(f"Unsupported method: {req.method}")

    res_data = res.json()
    # TODO: handle all of this in the class
    _res = cast_to_class(req, res_cls, **res_data)
    # _res = res_cls(
    #     data=res_data["data"],
    #     uuid=req.uuid,
    #     # orig_id=req.orig_id,
    # )
    return _res
