from fastapi import HTTPException

import models


def authorize(Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user


def generate_auth_token(Authorize, user):
    access_token = Authorize.create_access_token(subject=user.username)
    Authorize.set_access_cookies(access_token)
    return access_token


def fetch_user(db, email):
    fetchuser = db.query(models.User).filter(models.User.email == email).first()
    if fetchuser:
        setattr(fetchuser, "status", False)
        db.commit()
        msg = HTTPException(status_code=200, detail="User blocked")
    else:
        msg = HTTPException(status_code=400, detail="User not found")
    return msg


def fetch_all_users(db):
    return db.query(models.User).all()


def current_user_as_admin(username, db):
    check = db.query(models.Admin).filter(models.Admin.username == username).first()
    return check


def login(db, user,Authorize):
    check_admin = db.query(models.Admin).filter(models.Admin.username == user.username,
                                                models.Admin.password == user.password).first()
    if check_admin:
        access_token = generate_auth_token(Authorize, user)
        response = HTTPException(status_code=200, detail=access_token)
    else:
        response = HTTPException(status_code=400, detail="user not match")
    return response
