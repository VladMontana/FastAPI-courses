from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None
    schema: BaseModel = None
    
    def __init__(self, session):
        self.session = session
    
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)
    
    async def add_constructor(self, data: BaseModel):
        add_data = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data)
        model = result.scalars().one()
        return self.schema.model_validate(model)
    
    async def edit_constructor(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
        
    async def delete_constructor(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
    
    # Patch конструктор - на всякий случай  
    # async def patch_constructor(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
    #     patch_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
    #     await self.session.execute(patch_stmt)