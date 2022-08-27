# pylint: disable=import-error
"""Users module: Provides authentication and user management functionality"""

from pydantic import BaseModel
from authentication.hashing import Hasher

# TODO: Implement DB connection
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class UserCredentials(BaseModel):
    """User model: Username and password only"""
    username: str
    password: str


class CredentialsVerification(UserCredentials):
    """DatabaseUser model: Extends User with hashed password"""
    hashed_password: str


def get_verification(users_dict, username: str):
    """Gets a user by username"""
    if username in users_dict:
        user = users_dict[username]
        return CredentialsVerification(**user)
    return None


def login(username: str, password: str):
    """Authenticates a user by username and password"""
    user = get_verification(fake_users_db, username)

    if not user:
        return 'not found'

    verified = Hasher.verify_password(password, user.hashed_password)

    if not verified:
        return 'incorrect username or password'

    return True
