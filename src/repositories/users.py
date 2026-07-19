from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword, UserAdd
from src.repositories.mapper.mappers import UserDataMapper
from src.exception import UserAlreadyExistsException


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


    async def add_user(self, new_user_data: UserAdd):
        try:
            return await self.add_constructor(new_user_data)
        except IntegrityError:
            raise UserAlreadyExistsException()
        