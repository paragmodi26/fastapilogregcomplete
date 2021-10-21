from fastapi import FastAPI, Depends
from typing import List

from sqlalchemy.orm import Session

import models
from database import SessionLocal
from schema import UsersList
from user import useractions
from user_reg_log import reglogin

app = FastAPI()

app.include_router(reglogin.router)
app.include_router(useractions.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/all_user/", response_model=List[UsersList])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/")
def index():
    return "Welcome to Home page"
