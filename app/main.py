# pylint: disable=import-error
"""Main API routes. Includes routers for ML functions"""

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentication.users import create_access_token, get_current_user, get_verification, login
from data.database import create_tables
from data.settings import settings

from .routers import classification, users

PROTECTED = [Depends(get_current_user)]


def start_app():
    """Starts the app"""
    api = FastAPI(debug=True, title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION)

    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    api.include_router(classification.router,
                       dependencies=PROTECTED
                       )
    api.include_router(users.router)
    create_tables()
    return api


app = start_app()


@app.get("/")
def read_root():
    """Hello world"""
    return {"Hello": "World"}


@app.post("/token")
def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates and creates a new token from the given OAuth2 password request"""
    authenticated = login(form_data.username, form_data.password)

    if authenticated is True:
        user = get_verification(form_data.username)
        token = create_access_token(user)
        return {"access_token": token, "token_type": "bearer"}

    return {"error": "Wrong username or password"}
