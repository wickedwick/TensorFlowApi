# pylint: disable=import-error
"""User creation schema definition"""

from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    password: Optional[str] = None
