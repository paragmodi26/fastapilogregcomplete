from pydantic import BaseModel, EmailStr


class UsersList(BaseModel):
    id:int
    name: str
    number: str
    email: EmailStr
    age: int
    address: str
    status: bool

    class Config:
        orm_mode=True

