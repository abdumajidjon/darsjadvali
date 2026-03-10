"""Telegram bot package"""

from .dispatcher import get_dispatcher, get_bot
from .handlers import register_handlers

__all__ = ["get_dispatcher", "get_bot", "register_handlers"]
