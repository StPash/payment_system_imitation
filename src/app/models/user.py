from src.app.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(server_default="false")

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan",
                            lazy="joined")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan",
                            lazy="joined")
