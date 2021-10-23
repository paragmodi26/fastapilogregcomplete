from fastapi import HTTPException
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail

import models

conf = ConnectionConfig(
    MAIL_USERNAME="justforhost26@gmail.com",
    MAIL_PASSWORD="Modi3008@",
    MAIL_FROM="justforhost26@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_mail(user):
    print(user)
    message = MessageSchema(
        subject=user.subject,
        recipients=[user.email],
        subtype="html",
        html=user.message,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return HTTPException(status_code=200, detail="mail send")


def authorize(Authorize):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user


def generate_auth_token(Authorize, user):
    access_token = Authorize.create_access_token(subject=user.username)
    Authorize.set_access_cookies(access_token)
    return access_token


def blockuser(db, email):
    fetchuser = db.query(models.User).filter(models.User.email == email).first()
    if fetchuser:
        setattr(fetchuser, "status", False)
        db.commit()
        msg = HTTPException(status_code=200, detail="User blocked")
    else:
        msg = HTTPException(status_code=400, detail="User not found")
    return msg


def unblockuser(db, email):
    fetchuser = db.query(models.User).filter(models.User.email == email).first()
    if fetchuser:
        setattr(fetchuser, "status", True)
        db.commit()
        msg = HTTPException(status_code=200, detail="User Unblocked")
    else:
        msg = HTTPException(status_code=400, detail="User not found")
    return msg


def fetch_all_users(db):
    return db.query(models.User).all()


def checkuser(db, email):
    return db.query(models.User).filter(models.User.email == email).first()


def salary_post_add(db, user):
    check_user = checkuser(db, user.user_email)
    if check_user:
        checksalary = db.query(models.SalaryAndPost).filter(models.SalaryAndPost.user_email == user.user_email).first()
        if checksalary:
            setattr(checksalary, "salary", user.salary)
            setattr(checksalary,"post",user.post)
            db.commit()
            response=HTTPException(status_code=200,detail="User Data Update")
        else:
            obj = models.SalaryAndPost(**user.dict())
            db.add(obj)
            db.commit()
            db.refresh(obj)
            response = HTTPException(status_code=200, detail="User Data add")
    else:
        response = HTTPException(status_code=200, detail="User is not valid")
    return response


def current_user_as_admin(username, db):
    check = db.query(models.Admin).filter(models.Admin.username == username).first()
    return check


def login(db, user, Authorize):
    check_admin = db.query(models.Admin).filter(models.Admin.username == user.username,
                                                models.Admin.password == user.password).first()
    if check_admin:
        access_token = generate_auth_token(Authorize, user)
        response = HTTPException(status_code=200, detail=access_token)
    else:
        response = HTTPException(status_code=400, detail="user not match")
    return response


def user_delete(db, email):
    user_exists = checkuser(db, email)
    if user_exists:
        delete = db.query(models.User).filter(models.User.email == email).delete()
        if delete == 0:
            response = HTTPException(status_code=400, detail="user not delete")
        else:
            db.commit()
            response = HTTPException(status_code=200, detail="User Deleted")
    else:
        response = HTTPException(status_code=400, detail="user not found")
    return response
