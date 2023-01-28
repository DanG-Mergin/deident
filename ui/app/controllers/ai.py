import sys

sys.path.append("..")
from ..services import ai as ai_s
from ..schema import InternalMsg

# TODO: transform the request
async def deident(req: InternalMsg) -> InternalMsg:
    res = await ai_s.deident(req)
    return res
