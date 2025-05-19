from pydantic import BaseModel
from datetime import datetime
from chat.src.schemas.user import UserResponseSchema


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
    user_id: int
    timestampt: datetime
    is_readed: bool
