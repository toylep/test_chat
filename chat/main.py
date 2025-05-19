from fastapi import FastAPI
from chat.src.api.v1.router import api_router

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from chat.src.core.logger import setup_logger

logger = setup_logger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status: {response.status_code}")
        return response

app = FastAPI()
app.include_router(api_router)
