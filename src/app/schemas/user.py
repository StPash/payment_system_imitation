from typing import List, Optional

from pydantic import BaseModel, EmailStr

from src.app.schemas.account import SGettingAccount
from src.app.schemas.payment import SGettingPayment


class SBaseUser(BaseModel):
    email: EmailStr
    full_name: str


class SGettingUser(SBaseUser):
    id: int


class SGettingUserForAdmin(SGettingUser):
    is_admin: bool
    accounts: List[SGettingAccount]
    payments: List[SGettingPayment]


class SCreatingUser(SBaseUser):
    is_admin: bool = False
    password: str


class SUpdatingUser(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

