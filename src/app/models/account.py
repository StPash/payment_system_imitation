from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.app.database import Base


class Account(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(index=True)
    balance: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account", cascade="all, delete-orphan")
