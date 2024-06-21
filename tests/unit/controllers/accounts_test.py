import pytest
from unittest import mock
from fastapi.exceptions import HTTPException
from app.controllers.accounts import AccountController
from make_query_param_filters import MakeQueryFilters
from app.models.transfer_history import TransferHistory
from tests.mocks.accounts import (
    query_params,
    account_model,
    account,
    updated_account_model,
    update_info,
    transfer_info,
    transfer_info_insuficient_funds,
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
        return_value=account_model
    )
    session.execute.return_value.scalars.return_value.all = mock.MagicMock(
        return_value=[account_model]
    )

    return session


@mock.patch.object(MakeQueryFilters, "make_filters", return_value=set())
def test_get_filters(make_filters_mock):
    filters = AccountController(session=None)._AccountController__get_filters(
        query_params
    )
    assert filters == set()


@pytest.mark.asyncio
@mock.patch.object(
    AccountController, "_AccountController__get_filters", return_value=set()
)
async def test_count_accounts(get_filters_mock, session):
    number_of_accounts = await AccountController(session=session).count_accounts(
        query_params
    )

    session.execute.assert_called_once()
    session.execute.return_value.scalar.assert_called_once()
    assert number_of_accounts == 0


@pytest.mark.asyncio
@mock.patch.object(
    AccountController, "_AccountController__get_filters", return_value=set()
)
async def test_list_accounts(get_filters_mock, session):
    accounts = await AccountController(session=session).list_accounts(
        query_params, 1, 1
    )

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.all.assert_called_once()
    assert accounts == [account]


@pytest.mark.asyncio
async def test_create_account(session):
    new_account = await AccountController(session).create_account(account_model)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert new_account == account_model


@pytest.mark.asyncio
async def test_fetch_account(session):
    account = await AccountController(session).fetch_account(1)

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.first.assert_called_once()
    assert account == account_model


@pytest.mark.asyncio
async def test_update_balance(session):
    account = await AccountController(session).update_balance(
        updated_account_model, update_info
    )
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert account == updated_account_model


def test_check_transfer_balance(session):
    AccountController(session).check_transfer_balance(account, transfer_info)


def test_check_transfer_balance_with_insufficient_balance(session):
    with pytest.raises(HTTPException):
        AccountController(session).check_transfer_balance(
            account, transfer_info_insuficient_funds
        )


@pytest.mark.asyncio
async def test_transfer_balance(session):
    transfer_history = await AccountController(session).transfer_balance(
        account, account, transfer_info
    )

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    session.rollback.assert_not_called()
    assert type(transfer_history) is TransferHistory


@pytest.mark.asyncio
async def test_transfer_balance_exception(session):
    with pytest.raises(Exception):
        await AccountController(session).transfer_balance(
            account, account, transfer_info
        )

        session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_account(session):
    await AccountController(session).delete_account(account)

    session.delete.assert_called_once()
    session.commit.assert_called_once()
