# pylint: disable=import-error
"""User creation schema definition"""

from dataclasses import dataclass
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    password: Optional[str] = None


class UserShow(BaseModel):
    """User show schema"""
    username: str
    email: EmailStr
    is_active: bool

    @dataclass
    class Config():
        """Tells pydantic to convert even non dict obj to json"""
        orm_mode = True
