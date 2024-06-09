from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.database import get_session
from app.controllers.transfer_history import TransferHistoryController
from app.serializers.transfer_history import (
    QueryTransferHistorySerializer,
    ExportTransferHistoryList,
    ExportAccountTransferHistory,
    TransferHistorySerializer,
)
from app.serializers import QueryPagination
from app.serializers.auth import AuthTokenPayload
from app.utils.auth import auth_token
from app.utils.utils import next_page_url, previous_page_url

transfer_history_router = APIRouter(
    tags=["Transfer History"], prefix="/transfer_history"
)


@transfer_history_router.get("")
async def list_transfer_history(
    request: Request,
    query_params: QueryTransferHistorySerializer = Depends(),
    pagination: QueryPagination = Depends(),
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> ExportTransferHistoryList:
    controller = TransferHistoryController(session)
    request.url.replace(query=None)
    number_of_transfers = await controller.count_transfer_history(query_params)

    last_page = controller.get_last_page(number_of_transfers, pagination.page_size)

    if pagination.page > last_page and pagination.page > 1:
        pagination.page = last_page

    transfer_history = await controller.list_transfer_history(
        query_params,
        pagination.page_size,
        (pagination.page - 1) * pagination.page_size,
    )

    return ExportTransferHistoryList(
        page=pagination.page,
        page_size=pagination.page_size,
        next_page=next_page_url(
            pagination.page,
            pagination.page_size,
            number_of_transfers,
            request,
        ),
        previous_page=previous_page_url(
            pagination.page,
            pagination.page_size,
            number_of_transfers,
            request,
        ),
        total=number_of_transfers,
        transfer_history=transfer_history,
    )


@transfer_history_router.get("/{account_number}")
async def fetch_transfer_history_by_account_number(
    account_number: int,
    session: AsyncSession = Depends(get_session),
    _: AuthTokenPayload = Depends(auth_token),
) -> ExportAccountTransferHistory:
    return await TransferHistoryController(
        session
    ).fetch_transfer_history_by_account_number(account_number)  # type: ignore
