from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.configs.database import get_session
from app.utils.auth import OAuth2Controller
from app.serializers.auth import AuthToken, AuthSerializer
from app.controllers.auth import AuthController
from app.models.auth import Auth


auth_router = APIRouter(tags=["Auth"], prefix="/auth")


@auth_router.post("/login")
async def loggin(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session),
) -> AuthToken:
    if not await OAuth2Controller().authenticate(session, username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return OAuth2Controller().create_access_token(username)


@auth_router.post("", status_code=201)
async def create_auth(
    auth: AuthSerializer,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await AuthController(session).create(
            Auth(
                username=auth.username,
                password=OAuth2Controller().get_password_hash(auth.password),
            )
        )

    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already exists")
