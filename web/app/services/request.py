import httpx

# import asyncio
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder
from ..schema.base.messages import _Request
from ..schema.base.messages import _Response
from .utils import cast_to_class

client = httpx.AsyncClient()


async def make_request(req: _Request, res_cls: _Response) -> _Response:
    if req.method == "POST":
        res = await client.post(req.url, json=jsonable_encoder(req))
    elif req.method == "GET":
        res = await client.get(req.url)
    elif req.method == "PUT":
        res = await client.put(req.url, json=jsonable_encoder(req))
    elif req.method == "DELETE":
        res = await client.delete(req.url, json=jsonable_encoder(req))
    else:
        raise ValueError(f"Unsupported method: {req.method}")

    res_data = res.json()

    _res = cast_to_class(req, res_cls, **res_data)

    return _res
