"""APScheduler service for automated reminders, debt alerts and monthly reports."""
import logging
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from sqlalchemy import select, and_
from bot.config import settings
from bot.services.db import AsyncSessionLocal
from bot.models.user import User
from bot.models.debt import Debt
from bot.models.expense import Expense
from bot.models.reminder import Reminder
from bot.utils.i18n import t

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone=pytz.timezone(settings.TIMEZONE))

async def check_pending_reminders(bot: Bot) -> None:
    """Check and trigger pending reminders."""
    now = datetime.now()
    async with AsyncSessionLocal() as session:
        stmt = select(Reminder).where(
            and_(Reminder.is_sent == False, Reminder.remind_at <= now)
        )
        result = await session.execute(stmt)
        reminders = result.scalars().all()

        for rem in reminders:
            try:
                user = await session.get(User, rem.user_id)
                if user:
                    lang = user.language
                    msg = t("reminder_alert", lang, title=rem.title)
                    await bot.send_message(chat_id=user.telegram_id, text=msg, parse_mode="HTML")
                rem.is_sent = True
            except Exception as e:
                logger.error(f"Failed to send reminder {rem.id}: {e}")

        await session.commit()

async def check_debt_deadlines(bot: Bot) -> None:
    """Check debts nearing due date (1 day before and day of deadline)."""
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    async with AsyncSessionLocal() as session:
        stmt = select(Debt).where(Debt.is_closed == False, Debt.due_date.isnot(None))
        result = await session.execute(stmt)
        debts = result.scalars().all()

        for d in debts:
            if not d.due_date:
                continue
            due_d = d.due_date.date()
            if due_d == today or due_d == tomorrow:
                user = await session.get(User, d.user_id)
                if user:
                    lang = user.language
                    due_text = "bugun" if due_d == today else "ertaga"
                    if lang == "ru":
                        due_text = "сегодня" if due_d == today else "завтра"
                    elif lang == "uz_cyr":
                        due_text = "бугун" if due_d == today else "эртага"

                    msg = t(
                        "debt_reminder_alert",
                        lang,
                        person=d.person_name,
                        amount=d.amount,
                        due_text=due_text,
                    )
                    try:
                        await bot.send_message(chat_id=user.telegram_id, text=msg, parse_mode="HTML")
                    except Exception as e:
                        logger.error(f"Failed to send debt alert {d.id}: {e}")

async def send_monthly_summary(bot: Bot) -> None:
    """Send monthly financial summary to all active users."""
    now = datetime.now()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    async with AsyncSessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
        for u in users:
            stmt = select(Expense).where(
                and_(Expense.user_id == u.id, Expense.created_at >= first_day)
            )
            expenses = (await session.execute(stmt)).scalars().all()
            if not expenses:
                continue

            total = sum(e.amount for e in expenses)
            lang = u.language
            period = "Oylik xulosa" if lang == "uz_lat" else ("Ойлик хулоса" if lang == "uz_cyr" else "Месячный отчет")
            text = t("report_title", lang, period=period)
            text += t("report_total", lang, total=total)

            cat_map = {}
            for e in expenses:
                cat_map[e.category] = cat_map.get(e.category, 0.0) + e.amount

            text += t("report_by_category", lang)
            for cat, amt in cat_map.items():
                text += t("report_item", lang, category=cat, amount=amt)

            try:
                await bot.send_message(chat_id=u.telegram_id, text=text, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Failed to send monthly report to user {u.id}: {e}")

def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Setup and start scheduler jobs."""
    # Check reminders every 30 seconds
    scheduler.add_job(check_pending_reminders, "interval", seconds=30, args=[bot])
    # Check debt deadlines every morning at 09:00
    scheduler.add_job(check_debt_deadlines, "cron", hour=9, minute=0, args=[bot])
    # Send monthly report on the 1st day of every month at 10:00
    scheduler.add_job(send_monthly_summary, "cron", day=1, hour=10, minute=0, args=[bot])

    scheduler.start()
    return scheduler
