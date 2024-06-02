import pytest
from unittest import mock
from app.controllers.auth import AuthController
from tests.mocks.auth import (
    auth_model,
)


@pytest.fixture
def session():
    session = mock.AsyncMock()

    session.add = mock.MagicMock()
    session.commit = mock.AsyncMock()
    session.refresh = mock.AsyncMock()
    session.rerollback = mock.AsyncMock()
    session.execute = mock.AsyncMock()
    session.execute.return_value.scalar = mock.MagicMock(return_value=0)
    session.execute.return_value.scalars = mock.MagicMock()
    session.execute.return_value.scalars.return_value.first = mock.MagicMock(
        return_value=auth_model
    )
    session.execute.return_value.scalars.return_value.all = mock.MagicMock(
        return_value=[auth_model]
    )

    return session


@pytest.mark.asyncio
async def test_create_auth(session):
    new_auth = await AuthController(session).create_auth(auth_model)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert new_auth == auth_model


@pytest.mark.asyncio
async def test_fetch_auth(session):
    auth = await AuthController(session).fetch_auth(1)

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.first.assert_called_once()
    assert auth == auth_model
