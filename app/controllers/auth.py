from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth import Auth

from app.utils.base_controller import BaseController


class AuthController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create_auth(self, auth: Auth) -> Auth:
        self.__session.add(auth)
        await self.__session.commit()
        await self.__session.refresh(auth)
        return auth

    async def fetch_auth(self, username: str) -> Auth | None:
        result = await self.__session.execute(
            select(Auth).where(Auth.username == username)
        )
        return result.scalars().first()
