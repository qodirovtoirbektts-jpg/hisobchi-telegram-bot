"""i18n and User session middleware for aiogram 3."""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy import select
from bot.services.db import AsyncSessionLocal
from bot.models.user import User

class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_user: TgUser | None = data.get("event_from_user")
        if not event_user:
            return await handler(event, data)

        async with AsyncSessionLocal() as session:
            # Find or create user
            stmt = select(User).where(User.telegram_id == event_user.id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                user = User(
                    telegram_id=event_user.id,
                    full_name=event_user.full_name,
                    username=event_user.username,
                    language="uz_lat",
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)

            data["db_user"] = user
            data["lang"] = user.language
            data["db_session"] = session

            return await handler(event, data)
