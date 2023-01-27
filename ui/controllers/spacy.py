from ..services import spacy as spacy_s, utils

# TODO: transform the request
async def deident(req):
    res = await spacy_s.deident(req)
    return res
