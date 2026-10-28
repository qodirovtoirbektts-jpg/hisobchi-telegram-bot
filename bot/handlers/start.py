"""Start, help, and language selection handlers."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from bot.models.user import User
from bot.keyboards.inline import get_language_keyboard
from bot.utils.i18n import t
from bot.services.db import AsyncSessionLocal

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message, db_user: User, lang: str):
    """Handle /start command."""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    text = t("welcome", lang, name=user_name)
    await message.answer(text, parse_mode="HTML")

@router.message(Command("til"))
@router.message(Command("lang"))
async def cmd_language(message: Message, lang: str):
    """Handle language selection."""
    text = t("choose_language", lang)
    await message.answer(text, reply_markup=get_language_keyboard())

@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_language(callback: CallbackQuery, db_user: User):
    """Handle language change callback."""
    new_lang = callback.data.split(":")[1]
    async with AsyncSessionLocal() as session:
        user = await session.get(User, db_user.id)
        if user:
            user.language = new_lang
            await session.commit()

    confirm_text = t("lang_changed", new_lang)
    await callback.message.edit_text(confirm_text)
    await callback.answer()
