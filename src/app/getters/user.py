from src.app.models.user import User
from src.app.schemas import SGettingUserForAdmin, SGettingAccount, SGettingPayment


def get_user_for_admin(user: User) -> SGettingUserForAdmin:
    return SGettingUserForAdmin(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_admin=user.is_admin,
        accounts=[
            SGettingAccount(**account.to_dict()) for account in user.accounts
        ],
        payments=[
            SGettingPayment(**payment.to_dict()) for payment in user.payments
        ]

    )