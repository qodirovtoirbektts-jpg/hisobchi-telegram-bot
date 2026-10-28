"""Free-form text message handler."""
import logging
from aiogram import Router, F
from aiogram.types import Message
from bot.models.user import User
from bot.services.gemini import gemini_service
from bot.services.dispatcher import handle_parsed_result
from bot.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router(name="text")

@router.message(F.text, ~F.text.startswith("/"))
async def handle_text(message: Message, db_user: User, lang: str):
    """Process incoming text message."""
    try:
        result = await gemini_service.process_text(message.text)
        await handle_parsed_result(message, result, db_user, lang)
    except Exception as e:
        logger.error(f"Text handling error: {e}")
        await message.answer(t("error_occurred", lang))
