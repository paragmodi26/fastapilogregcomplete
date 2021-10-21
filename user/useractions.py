from typing import List

import bcrypt
from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import models
from database import SessionLocal
from user.schemas import UserLogin, Profile

app = FastAPI(
    prefix="/user",
    tags=['User Actions']
)
router = APIRouter(
    prefix="/user",
    tags=['User Actions']
)


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/login")
def user_login(user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    checkuser = db.query(models.User).filter(models.User.email == user.email).first()
    if checkuser:
        checkpassword = check_password(user.password, checkuser.password)
        if checkpassword is True:
            access_token = Authorize.create_access_token(subject=user.email)
            Authorize.set_access_cookies(access_token)
            return access_token
        else:
            return HTTPException(status_code=400, detail="Wrong Password")
    else:
        return HTTPException(status_code=400, detail="user not Found")


@router.get("/Home")
def user_home(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return f"welcome {current_user}"


@router.get('/profile', response_model=Profile)
def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    print(current_user)
    if current_user:
        user = db.query(models.User).filter(models.User.email == current_user).first()
        print(user.name)
        return user

@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}