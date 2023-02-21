import sys

sys.path.append("..")
from typing import List
from ..services import spacy as spacy_s
from ..schema.inbound.DeIDRequest import DeIDRequest
from ..schema.outbound.DeIDResponse import DeIDResponse


async def deID(req: DeIDRequest) -> List:
    annotations = await spacy_s.deID(req)

    return annotations
