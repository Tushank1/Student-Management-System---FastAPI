from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./student.db'
# SQLALCHEMY_DATABASE_URL = 'mongodb://tushankbhardwaj121:Mt7dZnU4UJsQxWCV@undefined/?replicaSet=atlas-dwzsuf-shard-0&ssl=true&authSource=admin'

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

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