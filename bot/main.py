"""Main entry-point for Hisobchi Telegram Bot."""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config import settings
from bot.services.db import init_db
from bot.services.scheduler import setup_scheduler
from bot.middlewares.i18n import I18nMiddleware
from bot.handlers import main_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("hisobchi_bot")

async def main() -> None:
    """Initialize resources and start bot polling."""
    logger.info("Initializing database...")
    await init_db()

    if not settings.BOT_TOKEN:
        logger.error(
            "XATOLIK: BOT_TOKEN topilmadi! Iltimos, Render.com da Environment Variables bo'limiga BOT_TOKEN ni kiriting."
        )
        return

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register Middlewares
    i18n_middleware = I18nMiddleware()
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)

    # Register Routers
    dp.include_router(main_router)

    # Start APScheduler
    logger.info("Starting scheduler...")
    setup_scheduler(bot)

    logger.info("Bot started polling successfully.")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
