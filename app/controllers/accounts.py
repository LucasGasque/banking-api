from fastapi.exceptions import HTTPException
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.accounts import Account
from app.serializers.accounts import (
    AccountSerializer,
    TransferInfo,
    UpdateAccountSerializer,
    QueryAccountSerializer,
)
from app.models.transfer_history import TransferHistory
from app.utils.make_filters import MakeQueryFilters
from app.utils.base_controller import BaseController


class AccountController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    def __get_filters(self, query_params: QueryAccountSerializer) -> set:
        return MakeQueryFilters.make_filters(
            integer_filters={
                Account.account_number: query_params.account_number,
                Account.owner_id: query_params.owner_id,
            },
        )

    async def count_accounts(self, query_params: QueryAccountSerializer) -> int:
        filters = self.__get_filters(query_params)
        result = await self.__session.execute(
            select(func.count(Account.account_number)).where(*filters)
        )
        return result.scalar() or 0

    async def list_accounts(
        self, query_params, limit: int, offset: int
    ) -> list[AccountSerializer]:
        filters: set = self.__get_filters(query_params)

        result = await self.__session.execute(
            select(Account)
            .where(*filters)
            .offset(offset)
            .limit(limit)
            .order_by(Account.account_number.desc())
        )

        return [
            AccountSerializer(**account.__dict__) for account in result.scalars().all()
        ]

    async def create_account(self, account: Account) -> Account:
        self.__session.add(account)
        await self.__session.commit()
        await self.__session.refresh(account)
        return account

    async def fetch_account(self, account_number: int) -> Account:
        result = await self.__session.execute(
            select(Account).where(Account.account_number == account_number)
        )

        account = result.scalars().first()

        self.verify_if_object_exists(account, "Account")

        return account  # type: ignore

    async def update_balance(
        self, account: Account, update_info: UpdateAccountSerializer
    ) -> Account:
        account.balance = update_info.balance

        await self.__session.commit()
        await self.__session.refresh(account)

        return account

    def check_transfer_balance(
        self,
        sending_account: Account,
        transfer_info: TransferInfo,
    ) -> None:
        if sending_account.balance < transfer_info.amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance in the sending account",
            )

    async def transfer_balance(
        self,
        sending_account: Account,
        receiving_account: Account,
        transfer_info: TransferInfo,
    ):
        try:
            receiving_account.balance += transfer_info.amount
            sending_account.balance -= transfer_info.amount

            transfer_history = TransferHistory(
                receiving_account_number=receiving_account.account_number,
                sending_account_number=sending_account.account_number,
                amount=transfer_info.amount,
            )

            self.__session.add(transfer_history)
            await self.__session.commit()
            await self.__session.refresh(transfer_history)

            return transfer_history

        except Exception as e:
            await self.__session.rollback()

            raise HTTPException(status_code=500, detail=str(e))

    async def delete_account(self, account: Account) -> None:
        await self.__session.delete(account)
        await self.__session.commit()
