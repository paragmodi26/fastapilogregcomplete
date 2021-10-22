import bcrypt
from fastapi import HTTPException

import models
from user_reg_log.functions import get_hashed_password


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def authorize(Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user


def check_user(db, user):
    return db.query(models.User).filter(models.User.email == user.email, models.User.status == True).first()


def login(db, user, Authorize):
    checkuser = check_user(db, user)
    if checkuser:
        checkpassword = check_password(user.password, checkuser.password)
        if checkpassword is True:
            access_token = Authorize.create_access_token(subject=user.email)
            Authorize.set_access_cookies(access_token)
            response = HTTPException(status_code=200, detail=access_token)
        else:
            response = HTTPException(status_code=400, detail="Wrong Password")
    else:
        response = HTTPException(status_code=400, detail="user not Found")
    return response


def profile_update(db, user, current_user):
    class UserEmail:
        email = current_user

    existing_item = check_user(db, UserEmail)
    if existing_item:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing_item, key, value)
        db.commit()
        response = HTTPException(status_code=200, detail="User Profile Update")
    else:
        response = HTTPException(status_code=400, detail="User not found")
    return response


def password_change(db, current_user, user):
    class UserEmail:
        email = current_user

    existing_user = check_user(db, UserEmail)
    if existing_user:
        passwordcheck = check_password(user.old_password, existing_user.password)
        if passwordcheck is True:
            hashed_password = get_hashed_password(user.password)
            setattr(existing_user, "password", hashed_password)
            db.commit()
            response = HTTPException(status_code=200, detail="password Change")
        else:
            response = HTTPException(status_code=200, detail="old password does not match")
    else:
        response = HTTPException(status_code=200, detail="user not found")
    return response
