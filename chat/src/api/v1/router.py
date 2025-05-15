from fastapi import APIRouter
from chat.src.core.config import settings
from chat.src.api.v1.endpoints.chat import router as chat_router
from chat.src.api.v1.endpoints.user import router as user_router

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(chat_router)
api_router.include_router(user_router)
