import bcrypt
from fastapi import HTTPException

import models


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def register_user(db, user):
    checkemail = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.number == user.number)).first()
    if checkemail:
        response = HTTPException(status_code=400, detail="User Already exists With this mail or Number")
    else:
        password = get_hashed_password(user.password)
        obj = models.User(name=user.name, number=user.number, email=user.email, age=user.age, gender=user.gender,
                          address=user.address, password=password)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        response = HTTPException(status_code=200, detail="user register Successfully")
    return response


def forgetpassword(db, user, email):
    check_user = db.query(models.User).filter(models.User.email == email).first()
    if check_user:
        hashed_password = get_hashed_password(user.password)
        setattr(check_user, "password", hashed_password)
        db.commit()
        response = HTTPException(status_code=200, detail="password change")
    else:
        response = HTTPException(status_code=400, detail="User not Found")
    return response
