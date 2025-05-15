from fastapi import FastAPI
from chat.src.api.v1.router import api_router

app = FastAPI()
app.include_router(api_router)
