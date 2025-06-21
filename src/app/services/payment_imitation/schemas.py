from pydantic import BaseModel


class SGettingSignatureData(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: int


class SPaymentWebhookObject(SGettingSignatureData):
    signature: str
