from fastapi import APIRouter, HTTPException, Response, Cookie

from src.app import schemas, crud
from src.app.deps import DbDependency
from src.app.utils.security import verify_password, get_access_token, get_refresh_token, decode_refresh_token

router = APIRouter()


@router.post(
    "/login/",
    response_model=schemas.SAccessToken,
    tags=["Вход и регистрация"],
    name="Войти по почте и паролю"
)
async def login(
        login_data: schemas.SLoginData,
        db: DbDependency,
        response: Response
):
    user = await crud.user.get_by(db=db, email=login_data.email)
    print(user)
    if not user or not verify_password(password_hash=user.password_hash, password=login_data.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    access_token = get_access_token(user.id)
    refresh_token = get_refresh_token(user.id)
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)
    return schemas.SAccessToken(access_token=access_token)


@router.post(
    "/refresh/",
    include_in_schema=True,
    response_model=schemas.SAccessToken,
    tags=["Вход и регистрация"],
    name="Обновить токен доступа"
    )
async def refresh_token(
    db: DbDependency,
    response: Response,
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token отсутствует")

    user_id = decode_refresh_token(refresh_token)

    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_access_token = get_access_token(user_id)
    response.set_cookie('access_token', new_access_token, httponly=True)

    return {"access_token": new_access_token}


@router.post(
    "/logout/",
    include_in_schema=True,
    status_code=204,
    tags=["Вход и регистрация"],
    name="Выйти из системы"
)
async def logout(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return None
