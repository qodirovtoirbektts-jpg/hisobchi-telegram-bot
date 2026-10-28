"""Expense confirmation and management handlers."""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.models.user import User
from bot.models.expense import Expense
from bot.services.pending import pop_pending_action
from bot.services.db import AsyncSessionLocal
from bot.utils.i18n import t

router = Router(name="expenses")

@router.callback_query(F.data.startswith("confirm:expense:"))
async def cb_confirm_expense(callback: CallbackQuery, db_user: User, lang: str):
    """Confirm and save pending expense."""
    action_id = callback.data.split(":")[2]
    pending = pop_pending_action(action_id)

    if not pending or pending.get("type") != "expense":
        await callback.answer(t("error_occurred", lang), show_alert=True)
        return

    data = pending["data"]
    async with AsyncSessionLocal() as session:
        expense = Expense(
            user_id=db_user.id,
            amount=data.get("amount", 0.0),
            category=data.get("category", "boshqa"),
            description=data.get("description", "")
        )
        session.add(expense)
        await session.commit()

    await callback.message.edit_text(t("expense_saved", lang))
    await callback.answer()

@router.callback_query(F.data.startswith("cancel:expense:"))
async def cb_cancel_expense(callback: CallbackQuery, lang: str):
    """Cancel pending expense."""
    action_id = callback.data.split(":")[2]
    pop_pending_action(action_id)
    await callback.message.edit_text(t("cancelled", lang))
    await callback.answer()
