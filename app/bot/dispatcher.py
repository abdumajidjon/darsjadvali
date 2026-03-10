"""Bot dispatcher setup"""

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.bot.handlers import register_handlers

# Global bot and dispatcher instances
_bot: Bot | None = None
_dispatcher: Dispatcher | None = None


def get_bot() -> Bot:
    """Get or create bot instance"""
    global _bot
    if _bot is None:
        _bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    return _bot


def get_dispatcher() -> Dispatcher:
    """Get or create dispatcher instance"""
    global _dispatcher
    if _dispatcher is None:
        bot = get_bot()
        _dispatcher = Dispatcher()
        register_handlers(_dispatcher)
    return _dispatcher
