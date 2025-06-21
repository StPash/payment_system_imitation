from fastapi import APIRouter

from src.app.api import login, user
from src.app.services.payment_imitation import payment_webhook


api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(user.router)
api_router.include_router(payment_webhook.router)
