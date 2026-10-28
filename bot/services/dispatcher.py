"""Intent dispatcher for processing parsed results from Gemini or text parser."""
from datetime import datetime
from aiogram.types import Message
from bot.models.user import User
from bot.models.reminder import Reminder
from bot.services.pending import create_pending_action
from bot.keyboards.inline import get_confirm_keyboard
from bot.services.db import AsyncSessionLocal
from bot.utils.i18n import t

async def handle_parsed_result(message: Message, result: dict, db_user: User, lang: str):
    """Route parsed intent into appropriate action and user confirmation."""
    intent_type = result.get("type", "unknown")
    data = result.get("data", {})

    if intent_type == "expense":
        amount = float(data.get("amount", 0.0))
        category = data.get("category", "boshqa")
        description = data.get("description", "-")

        action_id = create_pending_action("expense", data)
        text = t(
            "confirm_expense",
            lang,
            amount=amount,
            category=category,
            description=description,
        )
        keyboard = get_confirm_keyboard("expense", action_id, lang)
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    elif intent_type == "debt":
        person = data.get("person_name", "Noma'lum")
        amount = float(data.get("amount", 0.0))
        debt_type_key = "debt_given" if data.get("debt_type") == "given" else "debt_taken"
        debt_type_label = t(debt_type_key, lang)
        due_date_str = data.get("due_date") or t("no_due_date", lang)

        action_id = create_pending_action("debt", data)
        text = t(
            "confirm_debt",
            lang,
            person=person,
            amount=amount,
            debt_type=debt_type_label,
            due_date=due_date_str,
        )
        keyboard = get_confirm_keyboard("debt", action_id, lang)
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    elif intent_type == "reminder":
        title = data.get("title", "Eslatma")
        remind_at_raw = data.get("remind_at")
        remind_time = None
        if remind_at_raw:
            try:
                remind_time = datetime.strptime(remind_at_raw[:19], "%Y-%m-%d %H:%M:%S")
            except Exception:
                try:
                    remind_time = datetime.strptime(remind_at_raw[:10], "%Y-%m-%d")
                except Exception:
                    pass

        if not remind_time:
            remind_time = datetime.now()

        async with AsyncSessionLocal() as session:
            reminder = Reminder(
                user_id=db_user.id,
                title=title,
                remind_at=remind_time,
                reminder_type=data.get("reminder_type", "general"),
            )
            session.add(reminder)
            await session.commit()

        formatted_time = remind_time.strftime("%d.%m.%Y %H:%M")
        await message.answer(t("reminder_saved", lang, title=title, time=formatted_time), parse_mode="HTML")

    else:
        await message.answer(t("unknown_format", lang))
