from pydantic import BaseModel, EmailStr


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


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

