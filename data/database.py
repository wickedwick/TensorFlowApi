# pylint: disable=import-error
"""Database connections"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models.base import Base

# Uncomment follwing for PG database
# from data.settings import settings
# DATABASE_URL = settings.DATABASE_URL
# engine = create_engine(DATABASE_URL)

# Uncomment follwing for SQLLITE database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> sessionmaker:
    """Get the database instance"""
    try:
        db_instance = SessionLocal()
        return db_instance
    finally:
        db_instance.close()
