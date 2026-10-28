"""Debts listing, closing, and confirmation handlers."""
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy import select, and_
from bot.models.user import User
from bot.models.debt import Debt
from bot.keyboards.inline import get_debts_keyboard
from bot.services.pending import pop_pending_action
from bot.services.db import AsyncSessionLocal
from bot.utils.i18n import t

router = Router(name="debts")

@router.message(Command("qarzlar"))
@router.message(Command("debts"))
async def cmd_debts(message: Message, db_user: User, lang: str):
    """List active debts with close buttons."""
    async with AsyncSessionLocal() as session:
        stmt = select(Debt).where(and_(Debt.user_id == db_user.id, Debt.is_closed == False))
        result = await session.execute(stmt)
        debts = result.scalars().all()

    if not debts:
        await message.answer(t("debts_empty", lang))
        return

    text = t("debts_title", lang)
    for idx, d in enumerate(debts, 1):
        icon = "🔺" if d.debt_type == "given" else "🔻"
        due_str = d.due_date.strftime("%d.%m.%Y") if d.due_date else t("no_due_date", lang)
        text += t("debt_item", lang, index=idx, type_icon=icon, person=d.person_name, amount=d.amount, due_date=due_str)

    keyboard = get_debts_keyboard(debts, lang)
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("close_debt:"))
async def cb_close_debt(callback: CallbackQuery, db_user: User, lang: str):
    """Mark debt as paid / closed."""
    debt_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as session:
        debt = await session.get(Debt, debt_id)
        if debt and debt.user_id == db_user.id:
            debt.is_closed = True
            debt.closed_at = datetime.now()
            await session.commit()
            await callback.message.edit_text(t("debt_closed", lang))
            await callback.answer()
        else:
            await callback.answer(t("error_occurred", lang), show_alert=True)

@router.callback_query(F.data.startswith("confirm:debt:"))
async def cb_confirm_debt(callback: CallbackQuery, db_user: User, lang: str):
    """Confirm and save pending debt."""
    action_id = callback.data.split(":")[2]
    pending = pop_pending_action(action_id)

    if not pending or pending.get("type") != "debt":
        await callback.answer(t("error_occurred", lang), show_alert=True)
        return

    data = pending["data"]
    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"][:10], "%Y-%m-%d")
        except Exception:
            due_date = None

    async with AsyncSessionLocal() as session:
        debt = Debt(
            user_id=db_user.id,
            person_name=data.get("person_name", "Noma'lum"),
            amount=data.get("amount", 0.0),
            debt_type=data.get("debt_type", "given"),
            due_date=due_date
        )
        session.add(debt)
        await session.commit()

    await callback.message.edit_text(t("debt_saved", lang))
    await callback.answer()

@router.callback_query(F.data.startswith("cancel:debt:"))
async def cb_cancel_debt(callback: CallbackQuery, lang: str):
    """Cancel pending debt."""
    action_id = callback.data.split(":")[2]
    pop_pending_action(action_id)
    await callback.message.edit_text(t("cancelled", lang))
    await callback.answer()
