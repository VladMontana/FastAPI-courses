from src.services.jwt_service import JWTService
from src.services.base import BaseService
from src.schemas.users import UserRequestAdd, UserAdd, UserRequest
from src.exception import UserEmailAlreadyExistsException, InvalidPasswordException


class AuthService(BaseService):
    async def register_user(self, data: UserRequestAdd):
        hashed_password = JWTService().hash_password(data.password)
        new_user_data = UserAdd(
            email=data.email, hashed_password=hashed_password, username=data.username
        )
        await self.db.users.add_user(new_user_data)
        await self.db.commit()

    async def login_user(self, data: UserRequest):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserEmailAlreadyExistsException()
        if not JWTService().verify_password(data.password, user.hashed_password):
            raise InvalidPasswordException()
        access_token = JWTService().create_access_token({"user_id": user.id})

        return access_token

    async def get_me(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
