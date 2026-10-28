"""Voice message handler using Gemini AI."""
import io
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from bot.models.user import User
from bot.services.gemini import gemini_service
from bot.services.dispatcher import handle_parsed_result
from bot.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router(name="voice")

@router.message(F.voice)
async def handle_voice(message: Message, bot: Bot, db_user: User, lang: str):
    """Process incoming voice message."""
    try:
        status_msg = await message.answer("🎧 <i>Ovozli xabar tinglanmoqda va tahlil qilinmoqda...</i>", parse_mode="HTML")
        file_io = io.BytesIO()
        await bot.download(message.voice.file_id, destination=file_io)
        audio_data = file_io.getvalue()

        # Send to Gemini
        result = await gemini_service.process_audio(audio_data, mime_type="audio/ogg")
        await status_msg.delete()

        # Dispatch parsed intent
        await handle_parsed_result(message, result, db_user, lang)
    except Exception as e:
        logger.error(f"Voice handling error: {e}")
        await message.answer(t("error_occurred", lang))
