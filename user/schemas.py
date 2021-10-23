from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Item(BaseModel):
    salary: str
    post: str

    class Config:
        orm_mode = True


class Profile(BaseModel):
    id: int
    name: str
    number: str
    email: EmailStr
    age: int
    gender: str
    address: str
    status: bool
    salary: List[Item] = []

    class Config:
        orm_mode = True


class UpdateProfile(BaseModel):
    name: Optional[str]
    number: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    address: Optional[str]
    status: Optional[bool]

    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    old_password: str
    password: str

    class Config:
        orm_mode = True
