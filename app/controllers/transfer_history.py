from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transfer_history import TransferHistory
from app.serializers.transfer_history import (
    TransferHistorySerializer,
    QueryTransferHistorySerializer,
)
from app.models.accounts import Account
from app.utils.make_filters import MakeQueryFilters
from app.utils.base_controller import BaseController


class TransferHistoryController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __get_filters(self, query_params: QueryTransferHistorySerializer) -> set:
        return MakeQueryFilters.make_filters(
            integer_filters={
                TransferHistory.id: query_params.id,
                TransferHistory.receiving_account_number: query_params.receiving_account_number,
                TransferHistory.sending_account_number: query_params.sending_account_number,
            }
        )

    async def count_transfer_history(
        self, query_params: QueryTransferHistorySerializer
    ) -> int:
        filters = self.__get_filters(query_params)
        result = await self.__session.execute(
            select(func.count(TransferHistory.id)).where(*filters)
        )
        return result.scalar() or 0

    async def list_transfer_history(
        self, query_params, limit: int, offset: int
    ) -> list[TransferHistorySerializer]:
        filters: set = self.__get_filters(query_params)

        result = await self.__session.execute(
            select(TransferHistory)
            .where(*filters)
            .offset(offset)
            .limit(limit)
            .order_by(TransferHistory.id.desc())
        )

        return [
            TransferHistorySerializer(**transfer_history.__dict__)
            for transfer_history in result.scalars().all()
        ]

    async def fetch_transfer_history_by_account_number(
        self,
        account_number: int,
    ) -> Account:
        result = await self.__session.execute(
            select(Account)
            .options(joinedload(Account.receive_history))
            .options(joinedload(Account.send_history))
            .where(Account.account_number == account_number)
        )
        account = result.scalars().first()

        self.verify_if_object_exists(account, "Account")

        return account  # type: ignore
