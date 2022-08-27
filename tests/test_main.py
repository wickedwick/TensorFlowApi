# pylint: disable=import-error, missing-module-docstring, missing-function-docstring
from fastapi.testclient import TestClient
from app.main import app


def test_read_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_post_auth():
    client = TestClient(app)
    response = client.post(
        "/token",
        data={
            "username": "user",
            "password": "pass"
        },
        headers={
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "access_token", "token_type": "bearer"}
