from fastapi import APIRouter, Depends
from chat.src.db.dependencies import get_db
from chat.src.services.chat_service import ChatService
from chat.src.schemas.chat import ChatCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from chat.src.schemas.chat import ChatResponseSchema

from chat.src.services.dependencies import get_chat_service

router = APIRouter(prefix="/chat")


@router.get("/", response_model=list[ChatResponseSchema])
async def get_chats(service: ChatService = Depends(get_chat_service)):
    """
    Получаем чаты
    """
    return await service.get_all()


@router.post("/", response_model=ChatResponseSchema)
async def add_chat(
    schema: ChatCreateSchema, service: ChatService = Depends(get_chat_service)
):
    """
    Получаем чаты
    """
    return await service.add(schema)


@router.delete("/{id}", response_model=ChatResponseSchema)
async def delete_chat(id: int, service: ChatService = Depends(get_chat_service)):
    """
    Получаем чаты
    """
    return await service.delete(id)
