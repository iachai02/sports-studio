from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL", None)
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



