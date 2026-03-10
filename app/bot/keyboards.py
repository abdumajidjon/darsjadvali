"""Inline keyboards for bot"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_week_type_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting week type"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Toq hafta", callback_data="week_ODD"))
    builder.add(InlineKeyboardButton(text="Juft hafta", callback_data="week_EVEN"))
    builder.adjust(2)
    return builder.as_markup()


def get_day_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting day of week"""
    builder = InlineKeyboardBuilder()
    days = [
        ("Dushanba", 0),
        ("Seshanba", 1),
        ("Chorshanba", 2),
        ("Payshanba", 3),
        ("Juma", 4),
        ("Shanba", 5),
        ("Yakshanba", 6),
    ]
    
    for day_name, day_num in days:
        builder.add(InlineKeyboardButton(
            text=day_name,
            callback_data=f"day_{day_num}"
        ))
    
    builder.adjust(2)
    return builder.as_markup()
