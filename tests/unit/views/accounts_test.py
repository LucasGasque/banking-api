import pytest
from unittest import mock
from httpx import AsyncClient
from app.controllers.accounts import AccountController
from app.controllers.customer import CustomerController
from tests.mocks.accounts import (
    account,
    updated_account,
    account_json,
    updated_account_json,
)
from tests.mocks.transfer_history import transfer_history, transfer_history_json


BASE_ACCOUNT_URL = "/api/v1/accounts"


@pytest.mark.asyncio
@mock.patch.object(AccountController, "count_accounts", return_value=1)
@mock.patch.object(AccountController, "get_last_page", return_value=1)
@mock.patch.object(AccountController, "list_accounts", return_value=[account])
@mock.patch("app.views.accounts.next_page_url", return_value="next_page_url")
@mock.patch("app.views.accounts.previous_page_url", return_value="previous_page_url")
async def test_list_accounts(
    previous_page_url_mock,
    next_page_url_mock,
    list_accounts_mock,
    get_last_page_mock,
    count_accounts_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_ACCOUNT_URL}")
    assert response.status_code == 200
    assert response.json() == {
        "accounts": [account_json],
        "next_page": "next_page_url",
        "page": 1,
        "page_size": 10,
        "previous_page": "previous_page_url",
        "total": 1,
    }


@pytest.mark.asyncio
@mock.patch.object(AccountController, "fetch_account", return_value=account)
async def test_fetch_account(
    fetch_account_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_ACCOUNT_URL}/1")
    assert response.status_code == 200
    assert response.json() == account_json


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "fetch_customer", return_value=None)
@mock.patch.object(AccountController, "create_account", return_value=account)
async def test_create_account(
    create_account_mock,
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(f"{BASE_ACCOUNT_URL}", json=account_json)
    assert response.status_code == 201
    assert response.json() == account_json


@pytest.mark.asyncio
@mock.patch.object(AccountController, "fetch_account", return_value=account)
@mock.patch.object(AccountController, "update_balance", return_value=updated_account)
async def test_update_balance(
    update_balance_mock,
    fetch_account_mock,
    app_client: AsyncClient,
):
    response = await app_client.patch(
        f"{BASE_ACCOUNT_URL}",
        json={
            "account_number": 1,
            "balance": 500.0,
            "owner_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == updated_account_json


@pytest.mark.asyncio
@mock.patch.object(AccountController, "fetch_account", return_value=account)
@mock.patch.object(AccountController, "check_transfer_balance", return_value=None)
@mock.patch.object(AccountController, "transfer_balance", return_value=transfer_history)
async def test_transfer_amount(
    transfer_balance_mock,
    check_transfer_balance_mock,
    fetch_account_mock,
    app_client: AsyncClient,
):
    response = await app_client.patch(
        f"{BASE_ACCOUNT_URL}/transfer",
        json={
            "receiving_account_number": 1,
            "sending_account_number": 2,
            "amount": 100,
        },
    )
    assert response.status_code == 200
    assert response.json() == transfer_history_json


@pytest.mark.asyncio
@mock.patch.object(AccountController, "fetch_account", return_value=account)
@mock.patch.object(AccountController, "delete_account", return_value=None)
async def test_delete_account(
    delete_account_mock,
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.delete(f"{BASE_ACCOUNT_URL}/1")
    assert response.status_code == 204
