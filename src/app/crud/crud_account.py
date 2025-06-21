from src.app.crud.base_crud import CRUDBase
from src.app.models.account import Account


class CRUDAccount(CRUDBase):
    pass


account = CRUDAccount(Account)
