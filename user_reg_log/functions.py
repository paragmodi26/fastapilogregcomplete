import random

import bcrypt
from fastapi import HTTPException
from fastapi_mail import MessageSchema, FastMail

import models
from admin.functions import conf


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


def newpassword(db, user, email):
    check_user = db.query(models.User).filter(models.User.email == email).first()
    if check_user:
        hashed_password = get_hashed_password(user.password)
        setattr(check_user, "password", hashed_password)
        db.commit()
        response = HTTPException(status_code=200, detail="password change")
    else:
        response = HTTPException(status_code=400, detail="User not Found")
    return response


async def forgetpassword(db, user):
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user:
        otp = random.randint(1000, 9999)
        message = MessageSchema(
            subject="Otp For Password Change",
            recipients=[user.email],
            subtype="html",
            html="your otp for password change is " + str(otp) + ". Do not share Otp With anyone",
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        obj = models.Otp(otp=otp, user_email=user.email)
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return HTTPException(status_code=200, detail="Otp send please check your email")


def verifyotp(db, user):
    checkotp = db.query(models.Otp).filter(models.Otp.user_email == user.email, models.Otp.otp == user.otp,
                                           models.Otp.status == True).first()
    if checkotp:
        setattr(checkotp, "status", False)
        db.commit()
        response = HTTPException(status_code=200, detail="Otp Verify ENter new Pasword")
    else:
        response = HTTPException(status_code=200, detail="Invalid Otp")
    return response


