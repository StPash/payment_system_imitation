from pydantic import BaseModel


class SGettingPayment(BaseModel):
    id: int
    amount: int
    transaction_id: str


class SCreatingPayment(BaseModel):
    amount: int
    transaction_id: str
    account_id: int
    user_id: int


