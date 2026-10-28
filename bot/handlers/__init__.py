"""Handlers router aggregator."""
from aiogram import Router
from bot.handlers.start import router as start_router
from bot.handlers.expenses import router as expenses_router
from bot.handlers.debts import router as debts_router
from bot.handlers.reports import router as reports_router
from bot.handlers.voice import router as voice_router
from bot.handlers.text import router as text_router

main_router = Router(name="main")

# Include sub-routers in order of priority
main_router.include_router(start_router)
main_router.include_router(expenses_router)
main_router.include_router(debts_router)
main_router.include_router(reports_router)
main_router.include_router(voice_router)
main_router.include_router(text_router)
