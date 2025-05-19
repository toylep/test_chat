from fastapi import APIRouter, Depends
from chat.src.core.security import get_current_user
from chat.src.db.dependencies import get_db
from chat.src.schemas.user import UserResponseSchema
from chat.src.services.chat_service import ChatService
from chat.src.schemas.chat import ChatCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from chat.src.schemas.chat import ChatResponseSchema

from chat.src.services.dependencies import get_chat_service

router = APIRouter(prefix="/chat")


@router.get("/", response_model=list[ChatResponseSchema])
async def get_chats(
    service: ChatService = Depends(get_chat_service),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Получаем чаты
    """
    return await service.get_all_by_user(current_user)


@router.post("/", response_model=ChatResponseSchema)
async def add_chat(
    schema: ChatCreateSchema,
    service: ChatService = Depends(get_chat_service),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Получаем чаты
    """
    return await service.add(schema, current_user)

