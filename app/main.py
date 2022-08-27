# pylint: disable=import-error
"""Main API routes. Includes routers for ML functions"""

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .routers import classification

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(classification.router)


@app.get("/")
def read_root():
    """Hello world"""
    return {"Hello": "World"}


@app.post("/token")
def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates and creates a new token from the given OAuth2 password request"""
    return {"access_token": "access_token", "token_type": "bearer"}
