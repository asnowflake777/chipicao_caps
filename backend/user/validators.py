from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    password: str
    email: EmailStr


class CreatedUser(User):
    id: int


class UserToken(BaseModel):
    user_id: int
    token: str


class CreatedUserToken(BaseModel):
    id: int
    token: str
