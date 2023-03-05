from typing import List
from ..services import spacy as spacy_s
from ..schema.messages.inbound.DeIDRequest import DeIDRequest
from ..schema.messages.outbound.DeIDResponse import DeIDResponse


async def deID(req: DeIDRequest) -> List:
    annotations = await spacy_s.deID(req)

    return annotations
