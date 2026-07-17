from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from src.database import Base
from src.repositories.mapper.base import DataMapper

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, SchemaType]):
    model: type[ModelType]
    mapper: type[DataMapper[ModelType, SchemaType]]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_filtered(
        self,
        *filters: ColumnElement[bool],
        **filter_by: Any,
    ) -> list[SchemaType]:
        query = select(self.model).filter_by(**filter_by).filter(*filters)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self) -> list[SchemaType]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by: Any) -> SchemaType | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add_constructor(self, data: BaseModel) -> SchemaType:
        add_data = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        add_data = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data)

    async def edit_constructor(
        self,
        data: BaseModel,
        exclude_unset: bool = False,
        **filter_by: Any,
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    # Редактирование нескольких записей
    async def edit_bulk(
        self,
        data: Sequence[BaseModel],
    ) -> None:
        update_data = [item.model_dump() for item in data]
        if not update_data:
            return

        await self.session.execute(update(self.model), update_data)

    # Patch нескольких записей
    async def patch_bulk(
        self,
        data: Sequence[BaseModel],
    ) -> None:
        patch_data = [item.model_dump(exclude_unset=True) for item in data]
        if not patch_data:
            return

        await self.session.execute(update(self.model), patch_data)

    async def delete_constructor(self, **filter_by: Any) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    # Patch конструктор - на всякий случай
    # async def patch_constructor(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
    #     patch_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
    #     await self.session.execute(patch_stmt)
