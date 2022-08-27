"""Users module: Provides authentication and user management functionality"""

from pydantic import BaseModel

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


def fake_hash_password(password: str):
    """Placeholder for hash function"""
    return "hashed_password" + password


class User(BaseModel):
    """User model: Username and password only"""
    username: str
    password: str


class DatabaseUser(User):
    """DatabaseUser model: Extends User with hashed password"""
    hashed_password: str


def get_user(users_dict, username: str):
    """Gets a user by username"""
    if username in users_dict:
        user = users_dict[username]
        return DatabaseUser(**user)
    return None


def login(username: str, password: str):
    """Authenticates a user by username and password"""
    user = get_user(fake_users_db, username)
    print(fake_users_db)

    if not user:
        return 'not found'
    hashed_password = fake_hash_password(password)

    if not hashed_password == user.hashed_password:
        return 'incorrect username or password'

    return True
