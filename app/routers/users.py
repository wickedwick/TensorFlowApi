# pylint: disable=import-error
"""User management endpoints"""

from fastapi import APIRouter
from pydantic import BaseModel
from authentication.hashing import Hasher
from data.database import get_db
from data.models.users import User
from schemas.users import UserCreate, UserShow

router = APIRouter()


class UserProps(BaseModel):
    """User model properties"""
    user: UserCreate


@router.post("/create_user", status_code=201)
def create_user(props: UserProps):
    """
    Create a new user
    :param user:
    :param db:
    :return:
    """

    database = get_db()
    user = User(username=props.user.username,
                email=props.user.email,
                hashed_password=Hasher.hash_password(props.user.password),
                is_active=True,
                is_superuser=False,
                )

    database.add(user)
    database.commit()
    database.refresh(user)
