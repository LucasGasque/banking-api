from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.configs.database import Base


class TransferHistory(Base):
    __tablename__ = "transfer_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    receiving_account_number: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_number"),
        nullable=False,
    )
    sending_account_number: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_number"),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(nullable=False)
