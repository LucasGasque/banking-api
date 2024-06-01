from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import UTC, datetime, timedelta
from app.serializers.auth import AuthTokenPayload, AuthToken
from app.configs.settings import settings
from app.controllers.auth import AuthController


def auth_token(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")),
) -> AuthTokenPayload:
    token_body: dict = {}
    try:
        token_body = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    except JWTError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exception)
        )
    return AuthTokenPayload(**token_body)


class OAuth2Controller:
    def __init__(self):
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __verify_password(self, plain_password, hashed_password) -> bool:
        return self.__pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.__pwd_context.hash(password)

    async def authenticate(
        self, session: AsyncSession, username: str, password: str
    ) -> bool:
        user = await AuthController(session).fetch(username)
        if not user:
            return False
        if not self.__verify_password(password, user.password):
            return False
        return True

    def create_access_token(self, username: str) -> AuthToken:
        return AuthToken(
            access_token=jwt.encode(
                AuthTokenPayload(
                    username=username,
                    exp=datetime.timestamp(
                        datetime.now(UTC)
                        + timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                    ),
                ).__dict__,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM,
            )
        )
