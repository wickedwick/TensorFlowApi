# pylint: disable=import-error, missing-module-docstring, missing-function-docstring, missing-class-docstring, line-too-long
from fastapi.testclient import TestClient
from data.models.users import User

from app.main import app


class MockDb:
    def __init__(self):
        self.users = []

    def add(self, user):
        pass

    def commit(self):
        pass

    def refresh(self, user):
        pass


def test_create_user_invalid():
    client = TestClient(app)
    response = client.post(
        "/create_user",
        json={
            "user": {
                "name": "test"
            }
        }
    )

    assert response.status_code == 422


def test_create_user_success(mocker):
    mock_db = MockDb()
    mocker.patch('app.routers.users.get_db', return_value=mock_db)
    client = TestClient(app)
    response = client.post(
        "/create_user",
        json={
            "user": {
                "username": "usertest",
                "email": "usertest@test.com",
                "password": "password"
            }
        }
    )

    assert response.status_code == 201
