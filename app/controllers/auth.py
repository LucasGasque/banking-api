from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth import Auth
from app.serializers.auth import (
    BaseAuthSerializer,
)
from app.utils.base_controller import BaseController


class AuthController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, auth: Auth) -> BaseAuthSerializer:
        self.__session.add(auth)
        await self.__session.commit()
        await self.__session.refresh(auth)
        return BaseAuthSerializer(**auth.__dict__)

    async def fetch(self, username: str) -> Auth | None:
        result = await self.__session.execute(
            select(Auth).where(Auth.username == username)
        )
        return result.scalars().first()
