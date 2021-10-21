from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Profile(BaseModel):
    id:int
    name: str
    number: str
    email: EmailStr
    age: int
    address: str
    status: bool

    class Config:
        orm_mode = True
