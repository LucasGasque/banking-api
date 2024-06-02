from app.serializers.accounts import (
    AccountSerializer,
    QueryAccountSerializer,
    UpdateAccountBalanceSerializer,
    TransferInfo,
)
from app.models.accounts import Account


account = AccountSerializer(account_number=1, owner_id=1, balance=1000)
updated_account = AccountSerializer(account_number=1, owner_id=1, balance=5000)

account_json = {
    "account_number": 1,
    "balance": 1000.0,
    "owner_id": 1,
}

updated_account_json = {
    "account_number": 1,
    "balance": 5000.0,
    "owner_id": 1,
}

query_params = QueryAccountSerializer(account_number="1", owner_id="1")

account_model = Account(**account.model_dump())

updated_account_model = Account(**updated_account.model_dump())

update_info = UpdateAccountBalanceSerializer(balance=5000, account_number=1)

transfer_info = TransferInfo(
    receiving_account_number=1, amount=1000, sending_account_number=1
)

transfer_info_insuficient_funds = TransferInfo(
    receiving_account_number=1, amount=1001, sending_account_number=1
)
