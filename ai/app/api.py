# TODO: remove 
# import debugpy

# debugpy.listen(("0.0.0.0", 5678))
# print("Waiting for client to attach...")
# debugpy.wait_for_client()

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

sys.path.append(".")
from .controllers import spacy as spacy_c

# from ai.app import app as ai_app
# from frontend.app import app as ui_app
# from backend.app import app as data_app

app = FastAPI()
log = logging.getLogger(__name__)

origins = [
    "http://localhost:8082",
    "http://localhost:8083",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test():
    return {"Hello": "From ml_app"}


# TODO: add request object
# TODO: add response object
@app.get("/deident/")
async def deident(req):
    res = await spacy_c.deident(req)
    return res


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8083, log_level="info")