from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controllers.v1 import auth_controller, member_controller

app = FastAPI()

origins = [
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_controller.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(member_controller.router, prefix="/v1/members", tags=["Members"])
