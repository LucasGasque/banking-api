import pytest
from unittest import mock
from app.controllers.transfer_history import TransferHistoryController
from app.utils.make_filters import MakeQueryFilters
from tests.mocks.transfer_history import (
    query_params,
    transfer_history_model,
    transfer_history,
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
        return_value=transfer_history_model
    )
    session.execute.return_value.scalars.return_value.all = mock.MagicMock(
        return_value=[transfer_history_model]
    )

    return session


@mock.patch.object(MakeQueryFilters, "make_filters", return_value=set())
def test_get_filters(make_filters_mock):
    filters = TransferHistoryController(
        session=None
    )._TransferHistoryController__get_filters(query_params)
    assert filters == set()


@pytest.mark.asyncio
@mock.patch.object(
    TransferHistoryController,
    "_TransferHistoryController__get_filters",
    return_value=set(),
)
async def test_count_transfer_history(get_filters_mock, session):
    number_of_transfer_history = await TransferHistoryController(
        session=session
    ).count_transfer_history(query_params)

    session.execute.assert_called_once()
    session.execute.return_value.scalar.assert_called_once()
    assert number_of_transfer_history == 0


@pytest.mark.asyncio
@mock.patch.object(
    TransferHistoryController,
    "_TransferHistoryController__get_filters",
    return_value=set(),
)
async def test_list_transfer_history(get_filters_mock, session):
    transfer_historys = await TransferHistoryController(
        session=session
    ).list_transfer_history(query_params, 1, 1)

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.all.assert_called_once()
    assert transfer_historys == [transfer_history]


@pytest.mark.asyncio
async def test_fetch_transfer_history_by_account_number(session):
    await TransferHistoryController(
        session=session
    ).fetch_transfer_history_by_account_number(1)

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.first.assert_called_once()
