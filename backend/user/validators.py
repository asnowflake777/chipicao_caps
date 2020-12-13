from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    password: str
    email: EmailStr
