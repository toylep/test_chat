from pydantic import BaseModel


class GroupCreateSchema(BaseModel):
    """
    Схема создания чатов
    """

    # Оставил пустым группа из 2х человек вряд ли имеет название
    name: str | None = None
    members: list[int]


class GroupResponseSchema(BaseModel):
    """
    Схема отображения чата
    """

    id: int
    name: str | None
    creator_id: int
