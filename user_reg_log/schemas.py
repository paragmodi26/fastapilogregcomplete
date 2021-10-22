from pydantic import BaseModel, EmailStr


class UserRegIn(BaseModel):
    name: str
    number: str
    email: EmailStr
    age: int
    gender: str
    address: str
    password: str


class ForgetPassword(BaseModel):
    password: str

