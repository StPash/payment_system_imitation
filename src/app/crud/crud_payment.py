from src.app.crud.base_crud import CRUDBase
from src.app.models.payment import Payment


class CRUDPayment(CRUDBase):
    pass


payment = CRUDPayment(Payment)
