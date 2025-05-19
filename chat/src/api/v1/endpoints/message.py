from fastapi import APIRouter, Depends, Query
from chat.src.core.security import get_current_user
from chat.src.schemas.message import MessageResponseSchema
from chat.src.schemas.pagination import PaginatedResponse
from chat.src.schemas.user import UserResponseSchema
from chat.src.services.dependencies import get_message_service, get_user_service
from chat.src.services.message_service import MessageService
from chat.src.services.user_service import UserService
from chat.src.utils.email import send_email
import asyncio

router = APIRouter(prefix="/messages", tags=["messages"])


async def pagination_params(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    return {"page": page, "limit": limit}

async def email_broadcast(users: list[UserResponseSchema]):
    for user in users:
        await send_email(
            to=user.email,
            subject="Ваше сообщение было прочитано"
            )

@router.get("/history/{chat_id}",response_model=PaginatedResponse[MessageResponseSchema])
async def get_history(
    chat_id: int,
    pagination: dict[str, int] = Depends(pagination_params),
    current_user: UserResponseSchema = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service),
):

    return await message_service.get_message_history(
        chat_id=chat_id, pagination=pagination
    )


@router.get("/read/{chat_id}")
async def mark_messages_as_read(
    chat_id: int,
    current_user: UserResponseSchema = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service),
    user_service: UserService = Depends(get_user_service),
):
    ids = await message_service.mark_messages_as_read(
        chat_id=chat_id, user_id=current_user.id
    )
    users = await user_service.get_all_by_id(ids)
    asyncio.create_task(email_broadcast(users))
    return {"message":"ok"}
    
    

