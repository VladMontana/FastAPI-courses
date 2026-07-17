from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword
from src.repositories.mapper.mappers import UserDataMapper


class UsersRepository(BaseRepository[UsersORM, User]):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        return UserWithHashedPassword.model_validate(obj=model, from_attributes=True)
