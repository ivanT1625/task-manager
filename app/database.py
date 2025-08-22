from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator

DATABASE_URL = "sqlite:///./task.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # нужно для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()