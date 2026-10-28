"""Financial report handlers (/bugun, /hafta, /oy)."""
from datetime import datetime, time, timedelta
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, and_
from bot.models.user import User
from bot.models.expense import Expense
from bot.services.db import AsyncSessionLocal
from bot.utils.i18n import t

router = Router(name="reports")

async def generate_report(user_id: int, start_date: datetime, period_name: str, lang: str) -> str:
    """Generate summary text for given time period."""
    async with AsyncSessionLocal() as session:
        stmt = select(Expense).where(
            and_(Expense.user_id == user_id, Expense.created_at >= start_date)
        )
        result = await session.execute(stmt)
        expenses = result.scalars().all()

    if not expenses:
        return t("report_empty", lang)

    total = sum(e.amount for e in expenses)
    text = t("report_title", lang, period=period_name)
    text += t("report_total", lang, total=total)

    cat_map = {}
    for e in expenses:
        cat_map[e.category] = cat_map.get(e.category, 0.0) + e.amount

    text += t("report_by_category", lang)
    for cat, amt in cat_map.items():
        text += t("report_item", lang, category=cat, amount=amt)

    return text

@router.message(Command("bugun"))
@router.message(Command("today"))
async def cmd_today(message: Message, db_user: User, lang: str):
    """Today's report."""
    today_start = datetime.combine(datetime.now().date(), time.min)
    period = "Bugun" if lang == "uz_lat" else ("Бугун" if lang == "uz_cyr" else "Сегодня")
    report_text = await generate_report(db_user.id, today_start, period, lang)
    await message.answer(report_text, parse_mode="HTML")

@router.message(Command("hafta"))
@router.message(Command("week"))
async def cmd_week(message: Message, db_user: User, lang: str):
    """Weekly report."""
    week_start = datetime.now() - timedelta(days=7)
    period = "Haftalik" if lang == "uz_lat" else ("Ҳафталик" if lang == "uz_cyr" else "Неделя")
    report_text = await generate_report(db_user.id, week_start, period, lang)
    await message.answer(report_text, parse_mode="HTML")

@router.message(Command("oy"))
@router.message(Command("month"))
async def cmd_month(message: Message, db_user: User, lang: str):
    """Monthly report."""
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    period = "Oylik" if lang == "uz_lat" else ("Ойлик" if lang == "uz_cyr" else "Месяц")
    report_text = await generate_report(db_user.id, month_start, period, lang)
    await message.answer(report_text, parse_mode="HTML")
