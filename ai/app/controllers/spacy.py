import sys

sys.path.append("..")
from typing import List
from ..services import spacy as spacy_s
from ..schema.inbound.DeIdentRequest import DeIdentRequest
from ..schema.outbound.DeIdentResponse import DeIdentResponse


async def deident(req: DeIdentRequest) -> List:
    annotations = await spacy_s.deident(req)

    return annotations
