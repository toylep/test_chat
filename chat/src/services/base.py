"""
Эти классы я реализовал давно, потому что надоело писать постоянно запросы.
Они кочуют из проекта в проект и я решил использовать их и тут
"""

from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from abc import ABC
from chat.src.repositories.base import BaseRepository


# CreateDTO = TypeVar("CreateDTO", bound=BaseModel)
DTO = TypeVar("DTO", bound=BaseModel)
# Repository = TypeVar("Repository",bound=BaseRepository)


class BaseService[CreateDTO, Repository](ABC):
    response_schema: Type[DTO]

    def __init__(self, repo: Repository):
        self.repo = repo

    async def get_all(self) -> list[DTO]:
        items = await self.repo.get_all()
        return [self.response_schema.model_validate(item.__dict__) for item in items]

    async def get_by_id(self, item_id: int) -> DTO:
        item = await self.repo.get_with_filters({"id": item_id}, return_single=True)
        return self.response_schema.model_validate(item.__dict__) if item else None

    async def add(self, dto: CreateDTO) -> DTO:
        item = await self.repo.add(dto.model_dump())
        return self.response_schema.model_validate(item.__dict__)

    async def update(self, item_id: int, dto: CreateDTO) -> DTO:
        item = await self.repo.update(item_id, dto.model_dump())
        return self.response_schema.model_validate(item.__dict__)

    async def delete(self, item_id: int) -> DTO:
        item = await self.repo.delete(item_id)
        return self.response_schema.model_validate(item.__dict__)
