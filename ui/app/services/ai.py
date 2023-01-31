# from pydantic import ValidationError
# import os
# import sys

# sys.path.append("..")
# from ..schema.outbound.DeIdentRequest import DeIdentRequest
# from .request import make_request
# from .utils import cast_to_class


# async def deident(req: DeIdentRequest):
#     try:
#         res = await make_request(req, url=f"{os.environ['AI_DEIDENT_URL']}")
#     except ValidationError as e:
#         print(e)  # TODO: log this and handle completely

#     return res
