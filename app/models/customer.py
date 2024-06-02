from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.configs.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
