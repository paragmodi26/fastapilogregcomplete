from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), index=True, nullable=True)
    number = Column(String(10), index=True, nullable=False)
    email = Column(String(25), index=True)
    age = Column(String(25), index=True)
    gender = Column(String(25), index=True)
    address = Column(String(25), index=True, nullable=False)
    status = Column(String(25), index=True, default=True)
    password = Column(String(250), index=True)

    salary = relationship("SalaryAndPost", back_populates="user")


class SalaryAndPost(Base):
    __tablename__ = "salaryandpost"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    salary = Column(String(200), index=True, default="admin")
    post = Column(String(250), index=True)
    user_email = Column(Integer, ForeignKey("User.email"))

    user = relationship("User", back_populates="salary")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(200), index=True, default="admin")
    password = Column(String(250), index=True)


class Otp(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    otp = Column(String(200), index=True, default="admin")
    user_email = Column(String(250), index=True)
    status = Column(String(25), index=True, default=True)
