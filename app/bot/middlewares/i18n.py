"""Re-export I18nMiddleware for compatibility with app/ structure."""
from bot.middlewares.i18n import I18nMiddleware

__all__ = ["I18nMiddleware"]
