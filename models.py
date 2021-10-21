from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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
    address = Column(String(25), index=True,nullable=False)
    status = Column(String(25), index=True, default=True)
    password = Column(String(250), index=True)
