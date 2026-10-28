"""Unit tests for models and database operations."""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.models.base import Base
from bot.models.user import User
from bot.models.expense import Expense
from bot.models.debt import Debt

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.mark.asyncio
async def test_create_and_read_user_expense():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        user = User(telegram_id=12345678, full_name="Test User", language="uz_lat")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        expense = Expense(user_id=user.id, amount=15000.0, category="transport", description="metro")
        session.add(expense)

        debt = Debt(user_id=user.id, person_name="Akmal", amount=50000.0, debt_type="given")
        session.add(debt)
        await session.commit()

        assert user.id is not None
        assert expense.id is not None
        assert debt.id is not None
        assert debt.is_closed is False
