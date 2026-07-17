from pydantic import BaseModel, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    username: str


class UserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    username: str


class User(BaseModel):
    id: int
    email: EmailStr
    username: str


class UserWithHashedPassword(User):
    hashed_password: str
