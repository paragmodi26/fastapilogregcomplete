from pydantic import BaseModel, EmailStr


class UserRegIn(BaseModel):
    name: str
    number: str
    email: EmailStr
    age: int
    gender: str
    address: str
    password: str


class RequestOtp(BaseModel):
    email: EmailStr


class VerifyOtp(BaseModel):
    email: EmailStr
    otp: str


class ForgetPassword(BaseModel):
    password: str


class SendMailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

    class Config:
        orm_mode = True
