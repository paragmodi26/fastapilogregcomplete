from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from user_reg_log.functions import register_user, forgetpassword
from user_reg_log.schemas import UserRegIn, ForgetPassword

router = APIRouter(prefix="/user", tags=['Users'])


@router.post("/register")
def user_register(user: UserRegIn, db: Session = Depends(get_db)):
    register = register_user(db, user)
    return register


@router.patch("/forgetpassword/{email}")
def forget_password(email, user: ForgetPassword, db: Session = Depends(get_db)):
    check_user = forgetpassword(db, user, email)
    return check_user
