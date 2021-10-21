
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from user_reg_log.schemas import UserRegIn


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/register")
def user_register(user: UserRegIn, db: Session = Depends(get_db)):
    checkemail = db.query(models.User).filter((models.User.email == user.email) | (models.User.number == user.number)).first()
    if checkemail:
        return HTTPException(status_code=400, detail="User Already exists With this mail")
    else:
        password = get_hashed_password(user.password)
        obj = models.User(name=user.name, number=user.number, email=user.email, age=user.age, gender=user.gender,
                          address=user.address, password=password)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return "user register Successfully"
