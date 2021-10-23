from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.util import asyncio

from database import SessionLocal, get_db
from user_reg_log.functions import register_user, forgetpassword, newpassword, verifyotp
from user_reg_log.schemas import UserRegIn, ForgetPassword, RequestOtp, VerifyOtp

router = APIRouter(prefix="/user", tags=['Users'])


@router.post("/register")
def user_register(user: UserRegIn, db: Session = Depends(get_db)):
    register = register_user(db, user)
    return register


@router.post('/forget-password/')
def forget_password(user: RequestOtp, db: Session = Depends(get_db)):
    check_user = asyncio.run(forgetpassword(db, user))
    return check_user

@router.post('/verify-otp/')
def forget_password(user: VerifyOtp, db: Session = Depends(get_db)):
    return verifyotp(db, user)



@router.patch("/new-password/{email}")
def new_password(email, user: ForgetPassword, db: Session = Depends(get_db)):
    check_user = newpassword(db, user, email)
    return check_user
