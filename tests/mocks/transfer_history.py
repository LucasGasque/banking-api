from app.serializers.transfer_history import (
    TransferHistorySerializer,
    ExportAccountTransferHistory,
    QueryTransferHistorySerializer,
)
from app.models.transfer_history import TransferHistory


transfer_history = TransferHistorySerializer(
    id=1, receiving_account_number=1, sending_account_number=2, amount=100
)

account = ExportAccountTransferHistory(
    owner_id=1,
    account_number=1,
    balance=100,
    receive_history=[transfer_history],
    send_history=[transfer_history],
)

transfer_history_json = {
    "amount": 100.0,
    "id": 1,
    "receiving_account_number": 1,
    "sending_account_number": 2,
}

account_json = {
    "account_number": 1,
    "balance": 100.0,
    "owner_id": 1,
    "receive_history": [
        {
            "amount": 100.0,
            "id": 1,
            "receiving_account_number": 1,
            "sending_account_number": 2,
        },
    ],
    "send_history": [
        {
            "amount": 100.0,
            "id": 1,
            "receiving_account_number": 1,
            "sending_account_number": 2,
        },
    ],
}

query_params = QueryTransferHistorySerializer(
    id="1", receiving_account_number="1", sending_account_number="2"
)

transfer_history_model = TransferHistory(**transfer_history.model_dump())
