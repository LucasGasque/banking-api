from app.configs.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Auth(Base):
    __tablename__ = "auth"

    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
