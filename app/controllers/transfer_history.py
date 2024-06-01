from sqlalchemy import func, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transfer_history import TransferHistory
from app.serializers.transfer_history import (
    TransferHistorySerializer,
)
from app.utils.make_filters import MakeQueryFilters
from app.utils.base_controller import BaseController


class TransferHistoryController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __get_filters(self, query_params) -> set:
        return MakeQueryFilters.make_filters(
            integer_filters={
                TransferHistory.id: query_params.id,
                TransferHistory.receiving_account_number: query_params.receiving_account_number,
                TransferHistory.sending_account_number: query_params.sending_account_number,
            }
        )

    def create(self, transfer_history: TransferHistory) -> None:
        self.__session.add(transfer_history)

    async def count_transfer_historys(self, query_params) -> int:
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
    ) -> list[TransferHistorySerializer]:
        result = await self.__session.execute(
            select(TransferHistory).where(
                or_(
                    TransferHistory.sending_account_number == account_number,
                    TransferHistory.receiving_account_number == account_number,
                )
            )
        )
        return [
            TransferHistorySerializer(**transfer_history.__dict__)
            for transfer_history in result.scalars().all()
        ]
