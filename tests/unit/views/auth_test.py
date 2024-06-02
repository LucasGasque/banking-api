import pytest
from unittest import mock
from httpx import AsyncClient
from sqlalchemy.exc import IntegrityError

from app.controllers.auth import AuthController
from app.utils.auth import OAuth2Controller
from tests.mocks.auth import auth, auth_json, token, token_json


BASE_AUTH_URL = "/api/v1/auth"


@pytest.mark.asyncio
@mock.patch.object(AuthController, "create_auth", return_value=auth)
async def test_create_account(
    create_auth_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(
        f"{BASE_AUTH_URL}", json={**auth_json, "password": "verysecurepassword"}
    )
    assert response.status_code == 201
    assert response.json() == auth_json


@pytest.mark.asyncio
@mock.patch.object(
    AuthController,
    "create_auth",
    side_effect=IntegrityError(
        "Username already exists", params={}, orig=BaseException()
    ),
)
async def test_create_account_integrity_error(
    create_auth_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(
        f"{BASE_AUTH_URL}", json={**auth_json, "password": "verysecurepassword"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Username already exists"}


@pytest.mark.asyncio
@mock.patch.object(OAuth2Controller, "authenticate", return_value=True)
@mock.patch.object(OAuth2Controller, "create_access_token", return_value=token)
async def test_login(
    create_access_token_mock,
    authenticate_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(
        f"{BASE_AUTH_URL}/login", data={**auth_json, "password": "verysecurepassword"}
    )
    assert response.status_code == 200
    assert response.json() == token_json


@pytest.mark.asyncio
@mock.patch.object(OAuth2Controller, "authenticate", return_value=False)
@mock.patch.object(OAuth2Controller, "create_access_token", return_value=token)
async def test_unauthorized_login(
    create_access_token_mock,
    authenticate_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(
        f"{BASE_AUTH_URL}/login", data={**auth_json, "password": "verysecurepassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
