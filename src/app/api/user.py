from typing import List

from fastapi import APIRouter, HTTPException, Response, Path

from src.app import schemas, crud
from src.app.deps import DbDependency, CurrentUser, CurrentAdmin
from src.app.getters.user import get_user_for_admin
from src.app.utils.security import hash_password

router = APIRouter()

user_tags = ['Пользователи']
admin_tags = ['Администратор']


@router.get(
    "/users/me/",
    tags=user_tags,
    name="получить информацию о текущем пользователе",
    response_model=schemas.SGettingUser
)
async def get_current_user(
        current_user: CurrentUser
):
    return schemas.SGettingUser(**current_user.to_dict())


@router.get(
    "/users/me/accounts/",
    tags=user_tags,
    name="получить информацию о счетах текущего пользователя",
    response_model=List[schemas.SGettingAccount]
)
async def get_current_user_accounts(
        current_user: CurrentUser
):
    return [schemas.SGettingAccount(**account.to_dict()) for account in current_user.accounts]


@router.get(
    "/users/me/payments/",
    tags=user_tags,
    name="получить информацию о платежах текущего пользователя",
    response_model=List[schemas.SGettingPayment]
)
async def get_current_user_payments(
        current_user: CurrentUser
):
    return [schemas.SGettingPayment(**payment.to_dict()) for payment in current_user.payments]


@router.get(
    "/users/",
    tags=admin_tags,
    name="получить информацию о пользователях",
    response_model=List[schemas.SGettingUserForAdmin]
)
async def get_users(
        db: DbDependency,
        current_user: CurrentAdmin
):
    users = await crud.user.get_all(db=db)
    data = [
        get_user_for_admin(user) for user in users
    ]
    return data


@router.get(
    "/users/{user_id}/",
    tags=admin_tags,
    name="получить информацию о пользователе",
    response_model=schemas.SGettingUserForAdmin
)
async def get_user(
        db: DbDependency,
        current_user: CurrentAdmin,
        user_id: int = Path(...)

):
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail=f"Пользователь c id {user_id} не обнаружен")
    return get_user_for_admin(user)


@router.patch(
    "/users/{user_id}/",
    tags=admin_tags,
    name="обновить данные пользователя",
    response_model=schemas.SGettingUser
)
async def update_user(
        data: schemas.SUpdatingUser,
        db: DbDependency,
        current_user: CurrentAdmin,
        user_id: int = Path(...)

):
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail=f"Пользователь c id {user_id} не обнаружен")
    updating_data = data.model_dump(exclude_none=True)
    if data.password:
        password_hash = hash_password(data.pop("password"))
        updating_data["password_hash"] = password_hash
    user = await crud.user.update(db=db, db_obj=user, data=updating_data)
    return get_user_for_admin(user)


@router.delete(
    "/users/{user_id}/",
    tags=admin_tags,
    name="удалить пользователя",
    response_model=schemas.SGettingUser
)
async def delete_user(
        db: DbDependency,
        current_user: CurrentAdmin,
        user_id: int = Path(...)

):
    user = await crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail=f"Пользователь c id {user_id} не обнаружен")
    deleted_user = await crud.user.remove_obj(db=db, obj=user)
    return get_user_for_admin(user)


@router.post(
    "/users/",
    tags=admin_tags,
    name="создать пользователя",
    response_model=schemas.SGettingUser
)
async def delete_user(
        data: schemas.SCreatingUser,
        db: DbDependency,
        current_user: CurrentAdmin,

):
    password_hash = hash_password(data.password)
    created_data = data.model_dump()
    created_data.pop("password")
    created_data["password_hash"] = password_hash
    user = await crud.user.create(db=db, data=created_data)
    return get_user_for_admin(user)
