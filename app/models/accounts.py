from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.configs.database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_number: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    balance: Mapped[float] = mapped_column(default=0.0)
