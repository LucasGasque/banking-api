from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional
from app.serializers import Pageinfo


class BaseAccountSerializer(BaseModel):
    owner_id: int
    balance: float = Field(ge=0)


class AccountSerializer(BaseAccountSerializer):
    account_number: int


class CreateAccount(BaseAccountSerializer): ...


class UpdateAccountBalance(BaseModel):
    account_number: int
    balance: float = Field(ge=0)


class QueryAccountSerializer(BaseModel):
    account_number: Optional[str] = Field(
        Query(
            default=None,
            description="You can pass multiple values separated by commas",
        )
    )
    owner_id: Optional[str] = Field(
        Query(
            default=None,
            description="You can pass multiple values separated by commas",
        )
    )


class ExportAccountList(Pageinfo):
    total: int
    accounts: list[AccountSerializer]


class TransferInfo(BaseModel):
    receiving_account_number: int
    sending_account_number: int
    amount: float = Field(ge=0)
