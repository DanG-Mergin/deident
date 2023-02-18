# from pydantic import ValidationError
# import os
# import sys

# sys.path.append("..")
# from ..schema.messages.outbound.DeIDRequest import DeIDRequest
# from .request import make_request
# from .utils import cast_to_class


# async def deID(req: DeIDRequest):
#     try:
#         res = await make_request(req, url=f"{os.environ['AI_DEIDENT_URL']}")
#     except ValidationError as e:
#         print(e)  # TODO: log this and handle completely

#     return res
