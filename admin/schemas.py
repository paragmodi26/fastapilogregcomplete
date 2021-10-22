from pydantic import BaseModel



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

