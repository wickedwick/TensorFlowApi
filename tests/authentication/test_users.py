# pylint: disable=import-error, missing-module-docstring, missing-function-docstring, redefined-outer-name
import pytest
from data.models.users import User
from authentication.users import login
# from authentication.users import CredentialsVerification, login, UserCredentials


@pytest.fixture
def test_password():
    return 'strong-password'


@pytest.fixture
def create_database_user(test_password: str):
    def make_user(**kwargs):
        kwargs['hashed_password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'test_user'
        if 'hashed_password' not in kwargs:
            kwargs['hashed_password'] = 'hashed_passwordsecret'
        return User(**kwargs)
    return make_user


def test_login_success(mocker, create_database_user):
    mocker.patch('authentication.users.get_verification',
                 return_value=create_database_user())
    mocker.patch('authentication.users.Hasher.verify_password',
                 return_value=True)
    result = login('ehonda', 'secret')
    assert result is True


def test_login_not_found(mocker):
    mocker.patch('authentication.users.get_verification',
                 return_value=None)
    result = login('ehonda', 'secret')
    assert result == 'not found'


def test_login_incorrect_password(mocker, create_database_user):
    mocker.patch('authentication.users.get_verification',
                 return_value=create_database_user())
    mocker.patch('authentication.users.Hasher.verify_password',
                 return_value=False)
    result = login('ehonda', 's3cr3t')
    assert result == 'incorrect username or password'
