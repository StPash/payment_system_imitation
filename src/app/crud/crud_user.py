from src.app.crud.base_crud import CRUDBase
from src.app.models.user import User


class CRUDUser(CRUDBase):
    pass


user = CRUDUser(User)
