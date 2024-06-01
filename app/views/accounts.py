import asyncio
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_session
from app.models.accounts import Account
from app.controllers.accounts import AccountController
from app.controllers.customer import CustomerController
from app.serializers.accounts import (
    BaseAccountSerializer,
    AccountSerializer,
    QueryAccountSerializer,
    ExportAccountList,
    TransferInfo,
    UpdateAccountSerializer,
)
from app.serializers.transfer_history import TransferHistorySerializer
from app.serializers import QueryPagination
from app.serializers.auth import AuthTokenPayload
from app.utils.auth import auth_token
from app.utils.utils import next_page_url, previous_page_url

account_router = APIRouter(tags=["Accounts"], prefix="/accounts")


@account_router.get("")
async def list_accounts(
    request: Request,
    query_params: QueryAccountSerializer = Depends(),
    pagination: QueryPagination = Depends(),
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
):
    controller = AccountController(session)
    number_of_accounts = await controller.count_accounts(query_params)

    last_page = controller.get_last_page(number_of_accounts, pagination.page_size)

    if pagination.page > last_page and pagination.page > 1:
        pagination.page = last_page

    accounts = await controller.list_accounts(
        query_params,
        pagination.page_size,
        (pagination.page - 1) * pagination.page_size,
    )

    return ExportAccountList(
        page=pagination.page,
        page_size=pagination.page_size,
        next_page=next_page_url(
            pagination.page,
            pagination.page_size,
            number_of_accounts,
            request,
        ),
        previous_page=previous_page_url(
            pagination.page,
            pagination.page_size,
            number_of_accounts,
            request,
        ),
        total=number_of_accounts,
        accounts=accounts,
    )


@account_router.get("/{account_number}")
async def fetch_account(
    account_number: int,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> AccountSerializer:
    account = await AccountController(session).fetch_account(account_number)

    return AccountSerializer(**account.__dict__)


@account_router.post("", status_code=201)
async def create_account(
    account: BaseAccountSerializer,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> AccountSerializer:
    await CustomerController(session).fetch_customer(account.owner_id)

    new_account = await AccountController(session).create_account(
        Account(**account.model_dump())
    )

    return AccountSerializer(**new_account.__dict__)


@account_router.patch("/")
async def update_balance(
    transfer_info: UpdateAccountSerializer,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> AccountSerializer:
    controller = AccountController(session)

    account = await controller.fetch_account(transfer_info.account_number)

    updated_account = await controller.update_balance(account, transfer_info)

    return AccountSerializer(**updated_account.__dict__)


@account_router.patch("/transfer")
async def transfer_amount(
    transfer_info: TransferInfo,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> TransferHistorySerializer:
    controller = AccountController(session)

    receiving_account, sending_account = await asyncio.gather(
        controller.fetch_account(transfer_info.receiving_account_number),
        controller.fetch_account(transfer_info.sending_account_number),
    )

    transfer_history = await controller.transfer_balance(
        sending_account,
        receiving_account,
        transfer_info,
    )

    return TransferHistorySerializer(**transfer_history.__dict__)


@account_router.delete("/{account_number}", status_code=204)
async def delete_account(
    account_number: int,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> None:
    controller = AccountController(session)

    account = await controller.fetch_account(account_number)

    await controller.delete_account(account)
