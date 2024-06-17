from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_session
from app.models.customer import Customer
from app.controllers.customer import CustomerController
from app.serializers.customer import (
    QueryCustomerSerializer,
    ExportCustomerList,
    CustomerSerializer,
    CreateCustomer,
    UpdateCustomer,
)
from app.serializers import QueryPagination
from app.serializers.auth import AuthTokenPayload
from app.utils.auth import auth_token
from app.utils.utils import next_page_url, previous_page_url


customer_router = APIRouter(tags=["Customers"], prefix="/customers")


@customer_router.get("")
async def list_customers(
    request: Request,
    query_params: QueryCustomerSerializer = Depends(),
    pagination: QueryPagination = Depends(),
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> ExportCustomerList:
    controller = CustomerController(session)
    request.url.replace(query=None)
    number_of_customers = await controller.count_customers(query_params)

    last_page = controller.get_last_page(number_of_customers, pagination.page_size)

    if pagination.page > last_page and pagination.page > 1:
        pagination.page = last_page

    customers = await controller.list_customers(
        query_params,
        pagination.page_size,
        (pagination.page - 1) * pagination.page_size,
    )

    return ExportCustomerList(
        page=pagination.page,
        page_size=pagination.page_size,
        next_page=next_page_url(
            pagination.page,
            pagination.page_size,
            number_of_customers,
            request,
        ),
        previous_page=previous_page_url(
            pagination.page,
            pagination.page_size,
            number_of_customers,
            request,
        ),
        total=number_of_customers,
        customers=customers,
    )


@customer_router.get("/{customer_id}")
async def fetch_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> CustomerSerializer:
    return await CustomerController(session).fetch_customer(customer_id)  # type: ignore


@customer_router.post("", status_code=201)
async def create_customer(
    new_customer: CreateCustomer,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> CustomerSerializer:
    return await CustomerController(session).create_customer(
        Customer(**new_customer.model_dump())
    )  # type: ignore


@customer_router.patch("/{customer_id}")
async def update_customer(
    customer_id: int,
    values_to_update: UpdateCustomer,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> CustomerSerializer:
    controller = CustomerController(session)

    customer = await controller.fetch_customer(customer_id)

    return await controller.update_customer(customer, values_to_update)  # type: ignore


@customer_router.delete("/{customer_id}", status_code=204)
async def delete_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> None:
    controller = CustomerController(session)

    customer = await controller.fetch_customer(customer_id)

    return await controller.delete_customer(customer)
