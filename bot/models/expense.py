"""Expense model definition."""
from sqlalchemy import BigInteger, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.models.base import Base, TimestampMixin

class Expense(Base, TimestampMixin):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="boshqa", nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    user = relationship("User", back_populates="expenses")
