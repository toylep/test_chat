from pydantic import BaseModel
from chat.src.schemas.group import GroupCreateSchema


class ChatCreateSchema(BaseModel):
    """
    Схема создания чатов
    """

    # Оставил пустым тк личные чаты вряд ли могут иметь название
    name: str | None = None
    is_group: bool
    group: GroupCreateSchema


class ChatResponseSchema(BaseModel):
    """
    Схема отображения чата
    """

    id: int
    name: str | None
    is_group: bool
    group_id: int | None
