# pylint: disable=import-error
"""Users module: Provides authentication and user management functionality"""

from datetime import datetime, timedelta
from pathlib import Path

import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from data.database import get_db
from data.models.users import User
from pydantic import BaseModel, ValidationError
from schemas.token import TokenPayload

from authentication.hashing import Hasher

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


def get_verification(username: str):
    """Gets a user by username"""
    database = get_db()
    user = database.query(User).filter(User.username == username).first()
    if user is not None:
        return user
    return None


def create_access_token(user: User):
    """Creates a JWT token"""
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": str(user)}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def login(username: str, password: str):
    """Authenticates a user by username and password"""
    user = get_verification(username)

    if not user:
        return "not found"

    verified = Hasher.verify_password(password, user.hashed_password)

    if not verified:
        return "incorrect username or password"

    return True


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    """Gets the current user"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(payload["sub"])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            details="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    print(token_data.sub.split(":")[0])
    user = get_verification(token_data.sub.split(":")[0])
    print(user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
