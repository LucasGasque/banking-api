import pytest
from unittest import mock
from fastapi.exceptions import HTTPException
from app.utils.auth import auth_token, OAuth2Controller
from app.controllers.auth import AuthController
from tests.mocks.auth import auth_model


@pytest.fixture
def session():
    session = mock.AsyncMock()
    return session


def test_invalid_auth_token():
    with pytest.raises(HTTPException):
        auth_token("invalid_token")


def test_valid_auth_token():
    token = auth_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imx1Y2FzIiwiZXhwIjoxODQxNzYzNDQ3LjEwNTEzM30.AAoBio4ma-j0xNuD9Z-wLc_XWHBEbum0W7jkUfH5rek"
    )
    assert token.username == "lucas"


def test_verify_password():
    controller = OAuth2Controller()

    hash_password = OAuth2Controller().get_password_hash("verystrongpassword")
    assert controller._OAuth2Controller__verify_password(
        "verystrongpassword", hash_password
    )


@pytest.mark.asyncio
@mock.patch.object(AuthController, "fetch_auth", return_value=None)
async def test_authenticate_no_user(fetch_auth_mock, session):
    result = await OAuth2Controller().authenticate(session, "lucas", "password")
    assert not result


@pytest.mark.asyncio
@mock.patch.object(AuthController, "fetch_auth", return_value=auth_model)
@mock.patch.object(
    OAuth2Controller,
    "_OAuth2Controller__verify_password",
    return_value=False,
)
async def test_authenticate_wrong_password(
    verify_password_mock, fetch_auth_mock, session
):
    result = await OAuth2Controller().authenticate(session, "lucas", "wrongpassword")
    assert not result


@pytest.mark.asyncio
@mock.patch.object(AuthController, "fetch_auth", return_value=auth_model)
@mock.patch.object(
    OAuth2Controller,
    "_OAuth2Controller__verify_password",
    return_value=True,
)
async def test_authenticate(verify_password_mock, fetch_auth_mock, session):
    result = await OAuth2Controller().authenticate(session, "lucas", "password")
    assert result


def test_create_access_token():
    token = OAuth2Controller().create_access_token(username="lucas")
    assert token.token_type == "bearer"
    assert auth_token(token.access_token).username == "lucas"
