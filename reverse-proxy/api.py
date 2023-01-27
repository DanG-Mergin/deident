import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai.api import api as ai_api
from ui.api import api as ui_api
from backend.api import api as data_api

app = FastAPI()
log = logging.getLogger(__name__)

# origins = [
#     "http://localhost",
#     "http://localhost:8081",
#     "http://localhost:8089",
#     "http://localhost:8080",
#     "http://localhost:8001",
#     "http://localhost:8005",
#     "http://localhost:3001",
#     "http://localhost:3000",
# ]

origins = [
    "http://localhost:8082",
    "http://localhost:8083",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=deident_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: set up a frontend router
@app.get("/")
def read_root():
    return {"Hello": "from the core api"}


# app.mount("/ai", ai_api)
# app.mount("/data", data_api)
# app.mount("/ui", ui_api)
