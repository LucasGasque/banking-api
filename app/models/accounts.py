from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.configs.database import Base
from app.models.transfer_history import TransferHistory


class Account(Base):
    __tablename__ = "accounts"

    account_number: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    balance: Mapped[float] = mapped_column(default=0.0)

    receive_history: Mapped[list[TransferHistory]] = relationship(
        foreign_keys=TransferHistory.receiving_account_number,
    )
    send_history: Mapped[list[TransferHistory]] = relationship(
        foreign_keys=TransferHistory.sending_account_number,
    )
