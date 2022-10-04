# pylint: disable=import-error
"""User database class"""

from dataclasses import dataclass

from sqlalchemy import Boolean, Column, Integer, String
from data.models.base_class import Base


@dataclass
class User(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def __str__(self) -> str:
        return self.username + ':' + self.email
