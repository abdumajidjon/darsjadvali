"""Broadcast service with rate limiting"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError

from app.database.models import User, Substitution, Schedule, Group


class BroadcastService:
    """Service for broadcasting messages to users with rate limiting"""
    
    def __init__(self, bot: Bot, db_session: AsyncSession, max_concurrent: int = 25):
        """
        Initialize broadcast service.
        
        Args:
            bot: aiogram Bot instance
            db_session: Database session
            max_concurrent: Maximum concurrent requests (default: 25)
        """
        self.bot = bot
        self.db_session = db_session
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def get_users_by_group(self, group_id: str) -> list[User]:
        """
        Get all users in a group.
        
        Args:
            group_id: Group UUID
        
        Returns:
            List of User objects
        """
        result = await self.db_session.execute(
            select(User).where(User.group_id == group_id)
        )
        return list(result.scalars().all())
    
    async def format_substitution_message(
        self,
        substitution: Substitution,
        language: str = "uz"
    ) -> str:
        """
        Format substitution message for user.
        
        Args:
            substitution: Substitution object
            language: User language preference
        
        Returns:
            Formatted message text
        """
        # Load schedule with group info
        result = await self.db_session.execute(
            select(Schedule)
            .options(selectinload(Schedule.group))
            .where(Schedule.id == substitution.schedule_id)
        )
        schedule = result.scalar_one_or_none()
        
        if not schedule:
            return ""
        
        # Day names
        days_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
        days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        day_names = days_uz if language == "uz" else days_en
        day_name = day_names[schedule.day_of_week] if schedule.day_of_week < len(day_names) else f"Day {schedule.day_of_week + 1}"
        
        # Pair names
        pair_names_uz = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        pair_names_en = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}
        
        pair_names = pair_names_uz if language == "uz" else pair_names_en
        pair_name = pair_names.get(schedule.pair_number, str(schedule.pair_number))
        
        # Week type
        week_type_text = "Toq" if schedule.week_type == "ODD" else "Juft"
        if language == "en":
            week_type_text = "Odd" if schedule.week_type == "ODD" else "Even"
        
        # Format message
        if language == "uz":
            message = f"🔄 O'zgarish aniqlandi!\n\n"
            message += f"📅 {day_name}\n"
            message += f"🔢 {pair_name} juftlik\n"
            message += f"📆 {week_type_text} hafta\n"
            message += f"📅 Sana: {substitution.target_date}\n\n"
            
            if substitution.new_subject:
                message += f"📚 Fan: {substitution.new_subject}\n"
            if substitution.new_teacher:
                message += f"👤 O'qituvchi: {substitution.new_teacher}\n"
            if substitution.new_room:
                message += f"🏫 Xona: {substitution.new_room}\n"
        else:
            message = f"🔄 Substitution detected!\n\n"
            message += f"📅 {day_name}\n"
            message += f"🔢 {pair_name} pair\n"
            message += f"📆 {week_type_text} week\n"
            message += f"📅 Date: {substitution.target_date}\n\n"
            
            if substitution.new_subject:
                message += f"📚 Subject: {substitution.new_subject}\n"
            if substitution.new_teacher:
                message += f"👤 Teacher: {substitution.new_teacher}\n"
            if substitution.new_room:
                message += f"🏫 Room: {substitution.new_room}\n"
        
        return message
    
    async def send_message_with_rate_limit(
        self,
        user_id: int,
        text: str
    ) -> bool:
        """
        Send message to user with rate limiting.
        
        Args:
            user_id: Telegram user ID
            text: Message text
        
        Returns:
            True if sent successfully, False otherwise
        """
        async with self.semaphore:
            try:
                await self.bot.send_message(chat_id=user_id, text=text)
                return True
            except TelegramAPIError as e:
                # Log error but don't fail the entire broadcast
                print(f"Failed to send message to {user_id}: {e}")
                return False
            except Exception as e:
                print(f"Unexpected error sending to {user_id}: {e}")
                return False
    
    async def broadcast_substitution(
        self,
        substitution: Substitution
    ) -> dict:
        """
        Broadcast substitution notification to all affected users.
        
        Args:
            substitution: Substitution object
        
        Returns:
            Dictionary with broadcast statistics
        """
        # Get schedule with group
        result = await self.db_session.execute(
            select(Schedule)
            .where(Schedule.id == substitution.schedule_id)
        )
        schedule = result.scalar_one_or_none()
        
        if not schedule:
            return {"success": 0, "failed": 0, "total": 0}
        
        # Get all users in the group
        users = await self.get_users_by_group(schedule.group_id)
        
        if not users:
            return {"success": 0, "failed": 0, "total": 0}
        
        # Format message for each user's language preference
        messages_by_lang: dict[str, str] = {}
        tasks = []
        
        for user in users:
            # Get message in user's language
            if user.language not in messages_by_lang:
                messages_by_lang[user.language] = await self.format_substitution_message(
                    substitution,
                    user.language
                )
            
            message = messages_by_lang[user.language]
            
            # Create send task
            task = self.send_message_with_rate_limit(user.telegram_id, message)
            tasks.append(task)
        
        # Execute all sends concurrently with rate limiting
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successes and failures
        success = sum(1 for r in results if r is True)
        failed = len(results) - success
        
        return {
            "success": success,
            "failed": failed,
            "total": len(results)
        }
