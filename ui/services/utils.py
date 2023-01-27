# utils.py is for SHARED abstract work

from ...ai.api import deident_ai_fake

# TODO: define this structure better it's ugly as...
# TODO: add generic RequestObject
async def make_request(req):
    # TODO: write generic request code :D
    # req = {"msg": req, "endpoint": "ai"}

    res = await ask_ai(req)
    return res


async def ask_ai(req):
    # TODO: add generic response object
    res = await deident_ai_fake(req)
    return res
