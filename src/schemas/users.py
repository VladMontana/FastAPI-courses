from pydantic import BaseModel, EmailStr, ConfigDict


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    username: str  
    

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