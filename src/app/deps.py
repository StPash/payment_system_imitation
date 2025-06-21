from typing import Annotated

from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import crud
from src.app.database import get_session
from src.app.models.user import User
from src.app.utils.security import decode_access_token


DbDependency = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
        db: DbDependency,
        access_token: str | None = Cookie(None)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    user_id = decode_access_token(access_token)
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не обнаружен")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return current_user

CurrentAdmin = Annotated[User, Depends(get_current_admin)]
