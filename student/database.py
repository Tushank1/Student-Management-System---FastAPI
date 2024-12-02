from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://Student:STUDENT@localhost:5433/Student"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# tushankbhardwaj121
# Mt7dZnU4UJsQxWCV
# mongodb://tushankbhardwaj121:Mt7dZnU4UJsQxWCV@undefined/?replicaSet=atlas-dwzsuf-shard-0&ssl=true&authSource=admin