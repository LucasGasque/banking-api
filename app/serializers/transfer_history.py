from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional
from app.serializers import Pageinfo
from app.serializers.accounts import AccountSerializer


class BaseTransferHistorySerializer(BaseModel):
    receiving_account_number: int
    sending_account_number: int
    amount: float


class TransferHistorySerializer(BaseTransferHistorySerializer):
    id: int


class QueryTransferHistorySerializer(BaseModel):
    id: Optional[str] = Field(
        Query(
            default=None,
            description="You can pass multiple values separated by commas",
        )
    )

    receiving_account_number: Optional[str] = Field(
        Query(
            default=None,
            description="You can pass multiple values separated by commas",
        )
    )
    sending_account_number: Optional[str] = Field(
        Query(
            default=None,
            description="You can pass multiple values separated by commas",
        )
    )


class ExportTransferHistoryList(Pageinfo):
    total: int
    transfer_history: list[TransferHistorySerializer]


class ExportAccountTransferHistory(AccountSerializer):
    receive_history: list[TransferHistorySerializer]
    send_history: list[TransferHistorySerializer]


    class ConfigDict:
        from_attributes = True
