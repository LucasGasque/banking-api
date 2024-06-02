import pytest
from unittest import mock
from httpx import AsyncClient
from app.controllers.customer import CustomerController
from tests.mocks.customer import (
    customer,
    updated_customer,
    customer_json,
    updated_customer_json,
)


BASE_CUSTOMERS_URL = "/api/v1/customers"


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "count_customers", return_value=1)
@mock.patch.object(CustomerController, "get_last_page", return_value=1)
@mock.patch.object(CustomerController, "list_customers", return_value=[customer])
@mock.patch("app.views.customer.next_page_url", return_value="next_page_url")
@mock.patch("app.views.customer.previous_page_url", return_value="previous_page_url")
async def test_list_customers(
    previous_page_url_mock,
    next_page_url_mock,
    list_customers_mock,
    get_last_page_mock,
    count_customers_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_CUSTOMERS_URL}")
    assert response.status_code == 200
    assert response.json() == {
        "customers": [customer_json],
        "next_page": "next_page_url",
        "page": 1,
        "page_size": 10,
        "previous_page": "previous_page_url",
        "total": 1,
    }


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "fetch_customer", return_value=customer)
async def test_fetch_customer(
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.get(f"{BASE_CUSTOMERS_URL}/1")
    assert response.status_code == 200
    assert response.json() == customer_json


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "fetch_customer", return_value=None)
@mock.patch.object(CustomerController, "create_customer", return_value=customer)
async def test_create_customer(
    create_customer_mock,
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.post(f"{BASE_CUSTOMERS_URL}", json=customer_json)
    assert response.status_code == 201
    assert response.json() == customer_json


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "fetch_customer", return_value=customer)
@mock.patch.object(CustomerController, "update_customer", return_value=updated_customer)
async def test_update_customer(
    update_customer_mock,
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.patch(
        f"{BASE_CUSTOMERS_URL}/1",
        json={"name": "Mr Updated Test Customer"},
    )
    assert response.status_code == 200
    assert response.json() == updated_customer_json


@pytest.mark.asyncio
@mock.patch.object(CustomerController, "fetch_customer", return_value=customer)
@mock.patch.object(CustomerController, "delete_customer", return_value=None)
async def test_delete_customer(
    delete_customer_mock,
    fetch_customer_mock,
    app_client: AsyncClient,
):
    response = await app_client.delete(f"{BASE_CUSTOMERS_URL}/1")
    assert response.status_code == 204
