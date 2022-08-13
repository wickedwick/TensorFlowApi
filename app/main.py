from fastapi import FastAPI
from .routers import classification

app = FastAPI()

app.include_router(classification.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
