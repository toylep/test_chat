from pydantic import BaseModel
from datetime import datetime
from chat.src.schemas.user import UserResponse


class MessageSchema(BaseModel):
    """
    Схема сообщения для отображения в других схемах
    """

    id: int
    text: str
    chat_id: int
    user_id: int
    created_at: datetime
    is_watched: bool


class MessageCreateSchema(BaseModel):
    """
    Схема создания сообщения
    """

    text: str
    chat_id: int
    user_id: int


class MessageResponseSchema(BaseModel):
    """
    Схема сообщения для отображения
    """

    id: int
    text: str
    chat_id: int
    user: UserResponse
    created_at: datetime
    is_watched: bool
