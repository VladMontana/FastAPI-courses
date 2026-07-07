from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.repositories.mapper.base import DataMapper
class BaseRepository:
    model = None
    mapper: DataMapper = None
    
    def __init__(self, session):
        self.session = session
    
    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
            .filter(*filter)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
    
    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
    
    async def add_constructor(self, data: BaseModel):
        add_data = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data)
        
    
    async def edit_constructor(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
    
    # Редактирование нескольких записей
    async def edit_bulk(self, data: list[BaseModel], **filter_by):
        update_data = [update(self.model).filter_by(**filter_by).values(**item.model_dump()) for item in data]
        await self.session.execute(update_data)


    # Patch нескольких записей
    async def patch_bulk(self, data: list[BaseModel], **filter_by):
        patch_data = [update(self.model).filter_by(**filter_by).values(**item.model_dump(exclude_unset=True)) for item in data]
        await self.session.execute(patch_data)


    async def delete_constructor(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
    
    # Patch конструктор - на всякий случай  
    # async def patch_constructor(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
    #     patch_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
    #     await self.session.execute(patch_stmt)