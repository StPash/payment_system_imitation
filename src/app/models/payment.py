from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.app.database import Base


class Payment(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[int] = mapped_column(default=0)
    transaction_id: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    user = relationship("User", back_populates="payments")
    account = relationship("Account", back_populates="payments")
