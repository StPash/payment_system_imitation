import hashlib

from fastapi import APIRouter, HTTPException, Response, Query
from fastapi.responses import JSONResponse

from src.app.deps import DbDependency
from src.app.schemas import SCreatingPayment
from src.app.services.payment_imitation.schemas import SPaymentWebhookObject, SGettingSignatureData
from src.app.config import settings

from src.app import crud

router = APIRouter()

@router.post(
    "/webhook/",
    tags=["Вебхуки"],
    name="Обработка вебхука имитированной платежной системы",
)
async def webhook(
        webhook_data: SPaymentWebhookObject,
        db: DbDependency,
):
    """
    Проверка подписи входящего вебхука.
    Проверка повторной обработки платежа.
    Проверка существования счета, создание счета при отсутствии.
    Сохранение платежа в базу данных.
    Изменение баланса счета.

    Обработчик вебхука при неверной подписи или повторной отправке данных по платежу отдаёт статус 200,
    а не статус ошибки, так зачатую платежные системы, не получив в ответ статус 200, неоднократно повторно
    направляют этот же запрос.
    """
    webhook_data_dict = webhook_data.model_dump()
    signature = webhook_data_dict.pop("signature")
    signature_data = [str(webhook_data_dict[key]) for key in sorted(webhook_data_dict.keys())]
    signature_data.append(settings.SECRET_KEY_WEBHOOK)
    signature_data_string = ''.join(signature_data)
    expected_signature = hashlib.sha256(signature_data_string.encode()).hexdigest()
    if expected_signature != signature:
        return JSONResponse(
            status_code=200,
            content={"message": "Invalid signature"}
        )

    existing_payment = await crud.payment.get_by(db=db, transaction_id=webhook_data.transaction_id)
    if existing_payment:
        return JSONResponse(
            status_code=200,
            content={"message": "Платеж уже обработан"}
        )

    user = await crud.user.get(db=db, id=webhook_data.user_id)
    if not user:
        return JSONResponse(
            status_code=200,
            content={"message": f"Пользователя с id {webhook_data.user_id} не существует"}
        )

    account = await crud.account.get_by(db=db, user_id=webhook_data.user_id, account_id=webhook_data.account_id)
    if not account:
        account = await crud.account.create(
            db=db,
            data={"user_id": webhook_data.user_id, "account_id": webhook_data.account_id}
        )

    payment_info = SCreatingPayment(**webhook_data_dict)
    payment_data = payment_info.model_dump()
    payment_data["account_id"] = account.id
    payment = await crud.payment.create(
        db=db,
        data=payment_data
    )

    account.balance += webhook_data.amount
    await db.commit()
    await db.refresh(account)
    return JSONResponse(
        status_code=200,
        content={"message": "OK"}
    )


@router.post(
    "/get-sign/",
    tags=["Вебхуки"],
    name="Получить подпись для теста вебхука",
)
async def webhook(
        data: SGettingSignatureData
):
    data_dict = data.model_dump()
    signature_data = [str(data_dict[key]) for key in sorted(data_dict.keys())]
    signature_data.append(settings.SECRET_KEY_WEBHOOK)
    signature_data_string = ''.join(signature_data)
    signature = hashlib.sha256(signature_data_string.encode()).hexdigest()
    return JSONResponse(
        status_code=200,
        content={"signature": signature}
    )
