from .utils import make_request


async def deident(req):
    res = await make_request(req)
    return res
