from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy.util import asyncio

from admin.functions import current_user_as_admin, login, fetch_all_users, authorize, user_delete, blockuser, \
    unblockuser, send_mail, salary_post_add
from admin.schemas import AdminLogin, AllUsers, SendMailSchema, UserDataAdd
from database import get_db
from schema import Settings

router = APIRouter(prefix="/admin", tags=['Admin Actions'])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/login/')
def admin_login(user: AdminLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    response = login(db, user, Authorize)
    return response


@router.get('/all-users/', response_model=List[AllUsers])
def all_users(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    fetchuser = current_user_as_admin(current_user, db)
    if fetchuser:
        fetchallusers = fetch_all_users(db)
        return fetchallusers
    else:
        return HTTPException(status_code=400, detail="User not Auth")


@router.patch('/blockuser/{email}')
def block_user(email, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    checkuser = current_user_as_admin(current_user, db)
    if checkuser:
        response = blockuser(db, email)
    else:
        response = HTTPException(status_code=400, detail="You are not Auth to block user")
    return response


@router.patch('/unblockuser/{email}')
def unblock_user(email, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    checkuser = current_user_as_admin(current_user, db)
    if checkuser:
        response = unblockuser(db, email)
    else:
        response = HTTPException(status_code=400, detail="Your are not Authorize")
    return response


@router.delete('/delete-user/{email}')
def delete_user(email, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    checkuser = current_user_as_admin(current_user, db)
    if checkuser:
        return user_delete(db, email)


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.post('/add-salary-and-post/')
def add_salary_and_post(user: UserDataAdd, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    current_user = authorize(Authorize)
    checkuser = current_user_as_admin(current_user, db)
    if checkuser:
        return salary_post_add(db, user)


@router.post('/send-mail-to-user')
def mail_send(mail: SendMailSchema, Authorize: AuthJWT = Depends()):
    print("hiii")
    return asyncio.run(send_mail(mail))
