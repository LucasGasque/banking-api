import pytest_asyncio
from unittest import mock
from httpx import AsyncClient, ASGITransport
from app.__main__ import create_app
from app.configs.database import get_session
from app.utils.auth import auth_token


async def override_get_session():
    yield mock.AsyncMock()


def override_auth_token():
    return {"username": "teste"}


@pytest_asyncio.fixture
async def app_client():
    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[auth_token] = override_auth_token
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
