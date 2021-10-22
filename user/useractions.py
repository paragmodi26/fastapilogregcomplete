from fastapi import FastAPI, APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from database import get_db
from schema import Settings
from user.functions import login, authorize, check_user, profile_update, password_change
from user.schemas import UserLogin, Profile, UpdateProfile, PasswordChange

router = APIRouter(prefix="/user", tags=['User Actions'])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/login")
def user_login(user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return login(db, user, Authorize)


@router.get("/Home")
def user_home(Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    return f"welcome {current_user}"


@router.get('/profile', response_model=Profile)
def user(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    current_user = authorize(Authorize)

    class UserEmail:
        email = current_user

    user = check_user(db, UserEmail)
    return user


@router.patch('/updateprofile/')
def update_profile(user: UpdateProfile, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    return profile_update(db, user, current_user)


@router.patch('/change_password/')
def change_password(user: PasswordChange, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    return password_change(db, current_user, user)


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
