"""
Эти классы я реализовал давно, потому что надоело писать постоянно запросы.
Они кочуют из проекта в проект и я решил использовать их и тут
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from sqlalchemy.orm import joinedload


class BaseRepository(ABC):
    @abstractmethod
    async def get_all(self, joined_fields: List[Any] = None):
        raise NotImplementedError

    @abstractmethod
    async def get_with_filters(
        self,
        filter_by: dict,
        return_single: bool = False,
        joined_fields: List[Any] = None,
    ):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, update_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepo[Model](BaseRepository):
    model_cls: type[Model]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, joined_fields: List[Any] = None) -> list[Model]:
        stmt = select(self.model_cls)
        if joined_fields:
            stmt = stmt.options(*[joinedload(field) for field in joined_fields])
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_with_filters(
        self,
        filter_by: dict,
        return_single: bool = False,
        joined_fields: List[Any] = None,
    ) -> list[Model] | Model:
        filter_conditions = []
        for field, value in filter_by.items():
            column = getattr(self.model_cls, field)
            if isinstance(value, (list, tuple)):
                filter_conditions.append(column.in_(value))
            elif value == "not_none":
                filter_conditions.append(column.isnot(None))
            elif value == "none":
                filter_conditions.append(column.is_(None))
            else:
                filter_conditions.append(column == value)

        stmt = select(self.model_cls).where(and_(*filter_conditions))
        if joined_fields:
            stmt = stmt.options(*[joinedload(field) for field in joined_fields])

        result = await self.session.execute(stmt)
        return result.scalars().first() if return_single else result.scalars().all()

    async def add(self, data: dict) -> Model:
        instance = self.model_cls(**data)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, id: int, update_data: dict) -> Model:
        stmt = (
            update(self.model_cls)
            .where(self.model_cls.id == id)
            .values(**update_data)
            .returning(self.model_cls)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def delete(self, id: int) -> Model:
        stmt = (
            delete(self.model_cls)
            .where(self.model_cls.id == id)
            .returning(self.model_cls)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
