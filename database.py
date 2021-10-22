from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "mysql://root:@localhost:3306/database1810"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
connection = engine.connect()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()