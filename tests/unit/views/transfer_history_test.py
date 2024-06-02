import pytest
from unittest import mock
from httpx import AsyncClient
from app.controllers.transfer_history import TransferHistoryController
from tests.mocks.transfer_history import (
    account,
    account_json,
    transfer_history,
    transfer_history_json,
)


BASE_TRANSFER_HISTORY_URL = "/api/v1/transfer_history"


@pytest.mark.asyncio
@mock.patch.object(TransferHistoryController, "count_transfer_history", return_value=1)
@mock.patch.object(TransferHistoryController, "get_last_page", return_value=1)
@mock.patch.object(
    TransferHistoryController, "list_transfer_history", return_value=[transfer_history]
)
@mock.patch("app.views.transfer_history.next_page_url", return_value="next_page_url")
@mock.patch(
    "app.views.transfer_history.previous_page_url", return_value="previous_page_url"
)
async def test_list_transfer_history(
    previous_page_url_mock,
    next_page_url_mock,
    list_transfer_history_mock,
    get_last_page_mock,
    count_transfer_history_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_TRANSFER_HISTORY_URL}")
    assert response.status_code == 200
    assert response.json() == {
        "transfer_history": [transfer_history_json],
        "next_page": "next_page_url",
        "page": 1,
        "page_size": 10,
        "previous_page": "previous_page_url",
        "total": 1,
    }


@pytest.mark.asyncio
@mock.patch.object(
    TransferHistoryController,
    "fetch_transfer_history_by_account_number",
    return_value=account,
)
async def test_fetch_transfer_history_by_account_number(
    fetch_transfer_history_by_account_number_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_TRANSFER_HISTORY_URL}/1")
    assert response.status_code == 200
    assert response.json() == account_json
