from pydantic import BaseModel, EmailStr


class AdminLogin(BaseModel):
    username: str
    password: str


class AllUsers(BaseModel):
    id: int
    name: str
    number: str
    email: str
    age: int
    gender: str
    address: str
    status: bool

    class Config:
        orm_mode = True


class SendMailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

    class Config:
        orm_mode = True


class UserDataAdd(BaseModel):
    user_email: EmailStr
    salary: str
    post: str

    class Cofig:
        orm_mode = True
