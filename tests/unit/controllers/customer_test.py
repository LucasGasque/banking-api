import pytest
from unittest import mock
from app.controllers.customer import CustomerController
from make_query_param_filters import MakeQueryFilters
from tests.mocks.customer import (
    query_params,
    customer_model,
    customer,
    update_info,
    updated_customer_model,
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
        return_value=customer_model
    )
    session.execute.return_value.scalars.return_value.all = mock.MagicMock(
        return_value=[customer_model]
    )

    return session


@mock.patch.object(MakeQueryFilters, "make_filters", return_value=set())
def test_get_filters(make_filters_mock):
    filters = CustomerController(session=None)._CustomerController__get_filters(
        query_params
    )
    assert filters == set()


@pytest.mark.asyncio
@mock.patch.object(
    CustomerController, "_CustomerController__get_filters", return_value=set()
)
async def test_count_customers(get_filters_mock, session):
    number_of_customer = await CustomerController(session=session).count_customers(
        query_params
    )

    session.execute.assert_called_once()
    session.execute.return_value.scalar.assert_called_once()
    assert number_of_customer == 0


@pytest.mark.asyncio
@mock.patch.object(
    CustomerController, "_CustomerController__get_filters", return_value=set()
)
async def test_list_customers(get_filters_mock, session):
    customers = await CustomerController(session=session).list_customers(
        query_params, 1, 1
    )

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.all.assert_called_once()
    assert customers == [customer]


@pytest.mark.asyncio
async def test_create_customer(session):
    new_customer = await CustomerController(session).create_customer(customer_model)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert new_customer == customer_model


@pytest.mark.asyncio
async def test_fetch_customer(session):
    customer = await CustomerController(session).fetch_customer(1)

    session.execute.assert_called_once()
    session.execute.return_value.scalars.assert_called_once()
    session.execute.return_value.scalars.return_value.first.assert_called_once()
    assert customer == customer_model


@pytest.mark.asyncio
async def test_update_customer(session):
    customer = await CustomerController(session).update_customer(
        updated_customer_model, update_info
    )
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert customer == updated_customer_model


@pytest.mark.asyncio
async def test_delete_customer(session):
    await CustomerController(session).delete_customer(customer)

    session.delete.assert_called_once()
    session.commit.assert_called_once()
