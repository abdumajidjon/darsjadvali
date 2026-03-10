"""Background worker tasks using Taskiq"""

from datetime import date
import uuid
from taskiq import InMemoryBroker
from taskiq_redis import ListQueueBroker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload
from sqlalchemy import select
import asyncio

from app.config import settings
from app.services.parser import ScheduleParser
from app.services.diff_engine import DiffEngine
from app.services.broadcast import BroadcastService
from app.database.models import Substitution
from aiogram import Bot

# Initialize broker (Redis)
try:
    broker = ListQueueBroker(url=settings.redis_url)
except Exception:
    # Fallback to in-memory broker for development
    broker = InMemoryBroker()

# Database session factory for workers
worker_engine = create_async_engine(settings.database_url, echo=False)
WorkerSessionLocal = async_sessionmaker(
    worker_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@broker.task
async def process_schedule_upload(file_content: bytes, target_date: str | None = None):
    """
    Background task to process uploaded schedule file.
    
    Args:
        file_content: Raw bytes of Excel file
        target_date: Target date for substitutions (ISO format, defaults to today)
    """
    if target_date is None:
        target_date_obj = date.today()
    else:
        target_date_obj = date.fromisoformat(target_date)
    
    # Create database session
    async with WorkerSessionLocal() as session:
        try:
            # Parse the schedule
            parser = ScheduleParser(file_content)
            entries = parser.parse()
            
            # Detect substitutions
            diff_engine = DiffEngine(session)
            substitutions = await diff_engine.detect_substitutions(entries, target_date_obj)
            
            # Commit changes
            await session.commit()
            
            # Trigger broadcasts for each substitution
            for substitution in substitutions:
                await broadcast_substitution_task.kiq(
                    str(substitution.id)
                )
            
            return {
                "status": "success",
                "entries_parsed": len(entries),
                "substitutions_detected": len(substitutions)
            }
        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to process schedule: {str(e)}")


@broker.task
async def broadcast_substitution_task(substitution_id: str):
    """
    Background task to broadcast substitution notification.
    
    Args:
        substitution_id: UUID of substitution record
    """
    substitution_uuid = uuid.UUID(substitution_id)
    
    # Create database session
    async with WorkerSessionLocal() as session:
        try:
            # Load substitution with schedule
            result = await session.execute(
                select(Substitution)
                .options(selectinload(Substitution.schedule))
                .where(Substitution.id == substitution_uuid)
            )
            substitution = result.scalar_one_or_none()
            
            if not substitution:
                return {"status": "error", "message": "Substitution not found"}
            
            # Initialize bot and broadcast service
            bot = Bot(token=settings.bot_token)
            broadcast_service = BroadcastService(bot, session)
            
            # Broadcast
            stats = await broadcast_service.broadcast_substitution(substitution)
            
            await session.commit()
            await bot.session.close()
            
            return {
                "status": "success",
                "substitution_id": substitution_id,
                "broadcast_stats": stats
            }
        except Exception as e:
            await session.rollback()
            raise Exception(f"Failed to broadcast substitution: {str(e)}")
