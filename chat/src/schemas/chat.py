from pydantic import BaseModel
from chat.src.schemas.message import MessageSchema


class ChatCreateSchema(BaseModel):
    """
    Схема создания чатов
    """

    name: str
    is_group: bool


class ChatResponseSchema(BaseModel):
    """
    Схема отображения чата
    """

    id: int
    name: str
    is_group: bool
