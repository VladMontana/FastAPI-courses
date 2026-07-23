from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserRequest
from src.core.dependencies import UserIdDep, DBDep
from src.exception import (
    UserAlreadyExistsException,
    UserEmailAlreadyExistsException,
    InvalidPasswordException,
)
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data=data)
        return {"status": "OK"}
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    
    


@router.post("/login")
async def login_user(data: UserRequest, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data=data)
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except InvalidPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_me(user_id=user_id)


@router.post("/logout")
async def exit_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
