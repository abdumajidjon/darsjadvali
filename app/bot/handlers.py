"""Telegram bot handlers"""

from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from datetime import date

from app.database.connection import AsyncSessionLocal
from app.database.models import User, Schedule, Group
from app.utils.week_calculator import get_week_type
from app.bot.keyboards import get_week_type_keyboard, get_day_keyboard


from contextlib import asynccontextmanager

@asynccontextmanager
async def get_user_session():
    """Get database session for handlers"""
    async with AsyncSessionLocal() as session:
        yield session


async def cmd_start(message: Message):
    """Handle /start command"""
    async with get_user_session() as session:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            welcome_text = (
                "👋 Salom! Siz allaqachon ro'yxatdan o'tgansiz.\n\n"
                "📚 Dars jadvalini ko'rish uchun /schedule buyrug'ini bering."
            )
        else:
            # Create new user
            from app.database.models import User
            import uuid
            
            user = User(
                id=uuid.uuid4(),
                telegram_id=message.from_user.id,
                role="student",
                language="uz"
            )
            session.add(user)
            await session.commit()
            
            welcome_text = (
                "👋 Salom! Dars jadvali botiga xush kelibsiz!\n\n"
                "📚 Dars jadvalini ko'rish uchun /schedule buyrug'ini bering.\n"
                "⚙️ Guruhni o'rnatish uchun /setgroup buyrug'ini bering."
            )
        
        await message.answer(welcome_text)


async def cmd_schedule(message: Message):
    """Handle /schedule command"""
    async with get_user_session() as session:
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.group_id:
            await message.answer(
                "❌ Sizning guruhingiz o'rnatilmagan.\n"
                "⚙️ Guruhni o'rnatish uchun /setgroup buyrug'ini bering."
            )
            return
        
        # Get current week type
        current_week = get_week_type()
        
        # Get schedules for user's group and current week
        result = await session.execute(
            select(Schedule)
            .where(
                Schedule.group_id == user.group_id,
                Schedule.week_type == current_week
            )
            .order_by(Schedule.day_of_week, Schedule.pair_number)
        )
        schedules = result.scalars().all()
        
        if not schedules:
            await message.answer(
                f"📅 {current_week} hafta uchun dars jadvali topilmadi."
            )
            return
        
        # Format schedule
        days_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        pair_names = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        
        schedule_text = f"📚 Dars jadvali ({current_week} hafta)\n\n"
        
        current_day = None
        for schedule in schedules:
            if current_day != schedule.day_of_week:
                current_day = schedule.day_of_week
                day_name = days_uz[schedule.day_of_week] if schedule.day_of_week < len(days_uz) else f"Kun {schedule.day_of_week + 1}"
                schedule_text += f"\n📅 {day_name}\n"
                schedule_text += "─" * 20 + "\n"
            
            pair_name = pair_names.get(schedule.pair_number, str(schedule.pair_number))
            schedule_text += f"\n🔢 {pair_name} juftlik\n"
            
            if schedule.subject:
                schedule_text += f"📚 {schedule.subject}\n"
            if schedule.teacher:
                schedule_text += f"👤 {schedule.teacher}\n"
            if schedule.room:
                schedule_text += f"🏫 {schedule.room}\n"
        
        await message.answer(schedule_text, reply_markup=get_week_type_keyboard())


async def cmd_setgroup(message: Message):
    """Handle /setgroup command"""
    async with get_user_session() as session:
        # Get all groups
        result = await session.execute(select(Group))
        groups = result.scalars().all()
        
        if not groups:
            await message.answer("❌ Hech qanday guruh topilmadi.")
            return
        
        # Format groups list
        groups_text = "📋 Mavjud guruhlar:\n\n"
        for i, group in enumerate(groups, 1):
            groups_text += f"{i}. {group.name}\n"
        
        groups_text += "\n⚙️ Guruhni tanlash uchun /setgroup <guruh_nomi> buyrug'ini bering."
        
        await message.answer(groups_text)


async def cmd_setgroup_with_name(message: Message):
    """Handle /setgroup <group_name> command"""
    async with get_user_session() as session:
        # Extract group name from command
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.answer("❌ Guruh nomini kiriting: /setgroup <guruh_nomi>")
            return
        
        group_name = parts[1].strip()
        
        # Find group
        result = await session.execute(
            select(Group).where(Group.name == group_name)
        )
        group = result.scalar_one_or_none()
        
        if not group:
            await message.answer(f"❌ '{group_name}' nomli guruh topilmadi.")
            return
        
        # Get or create user
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            from app.database.models import User
            import uuid
            user = User(
                id=uuid.uuid4(),
                telegram_id=message.from_user.id,
                group_id=group.id,
                role="student",
                language="uz"
            )
            session.add(user)
        else:
            user.group_id = group.id
        
        await session.commit()
        
        await message.answer(
            f"✅ Guruh muvaffaqiyatli o'rnatildi: {group.name}\n\n"
            "📚 Dars jadvalini ko'rish uchun /schedule buyrug'ini bering."
        )


async def callback_week_type(callback: CallbackQuery):
    """Handle week type selection callback"""
    async with get_user_session() as session:
        week_type = callback.data.split("_")[1]  # week_ODD or week_EVEN
        
        # Get user
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.group_id:
            await callback.answer("❌ Guruh o'rnatilmagan", show_alert=True)
            return
        
        # Get schedules
        result = await session.execute(
            select(Schedule)
            .where(
                Schedule.group_id == user.group_id,
                Schedule.week_type == week_type
            )
            .order_by(Schedule.day_of_week, Schedule.pair_number)
        )
        schedules = result.scalars().all()
        
        if not schedules:
            await callback.answer(f"📅 {week_type} hafta uchun jadval topilmadi", show_alert=True)
            return
        
        # Format schedule
        days_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        pair_names = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        
        week_name = "Toq" if week_type == "ODD" else "Juft"
        schedule_text = f"📚 Dars jadvali ({week_name} hafta)\n\n"
        
        current_day = None
        for schedule in schedules:
            if current_day != schedule.day_of_week:
                current_day = schedule.day_of_week
                day_name = days_uz[schedule.day_of_week] if schedule.day_of_week < len(days_uz) else f"Kun {schedule.day_of_week + 1}"
                schedule_text += f"\n📅 {day_name}\n"
                schedule_text += "─" * 20 + "\n"
            
            pair_name = pair_names.get(schedule.pair_number, str(schedule.pair_number))
            schedule_text += f"\n🔢 {pair_name} juftlik\n"
            
            if schedule.subject:
                schedule_text += f"📚 {schedule.subject}\n"
            if schedule.teacher:
                schedule_text += f"👤 {schedule.teacher}\n"
            if schedule.room:
                schedule_text += f"🏫 {schedule.room}\n"
        
        await callback.message.edit_text(schedule_text, reply_markup=get_week_type_keyboard())
        await callback.answer()


def register_handlers(dp: Dispatcher):
    """Register all bot handlers"""
    
    # Commands
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_schedule, Command("schedule"))
    dp.message.register(cmd_setgroup, Command("setgroup"))
    dp.message.register(cmd_setgroup_with_name, F.text.startswith("/setgroup "))
    
    # Callbacks
    dp.callback_query.register(callback_week_type, F.data.startswith("week_"))
