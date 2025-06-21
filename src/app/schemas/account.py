from pydantic import BaseModel


class SGettingAccount(BaseModel):
    id: int
    account_id: int
    balance: int


