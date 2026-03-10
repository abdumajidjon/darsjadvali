"""Diff engine for substitution detection"""

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

from app.database.models import Schedule, Substitution, Group
from app.services.parser import ScheduleEntry


class DiffEngine:
    """Engine for detecting schedule changes and substitutions"""
    
    def __init__(self, db_session: AsyncSession):
        """
        Initialize diff engine.
        
        Args:
            db_session: Database session
        """
        self.db_session = db_session
    
    async def get_or_create_group(self, group_name: str) -> Group:
        """
        Get or create a group by name.
        
        Args:
            group_name: Group name
        
        Returns:
            Group instance
        """
        # Try to find existing group
        result = await self.db_session.execute(
            select(Group).where(Group.name == group_name)
        )
        group = result.scalar_one_or_none()
        
        if group:
            return group
        
        # Create new group
        group = Group(id=uuid.uuid4(), name=group_name)
        self.db_session.add(group)
        await self.db_session.flush()
        return group
    
    async def get_current_schedules(self, group_id: uuid.UUID) -> dict[str, Schedule]:
        """
        Get current schedules for a group, indexed by key.
        
        Args:
            group_id: Group UUID
        
        Returns:
            Dictionary with key format: "day_pair_week" -> Schedule
        """
        result = await self.db_session.execute(
            select(Schedule).where(Schedule.group_id == group_id)
        )
        schedules = result.scalars().all()
        
        schedule_dict = {}
        for schedule in schedules:
            key = f"{schedule.day_of_week}_{schedule.pair_number}_{schedule.week_type}"
            schedule_dict[key] = schedule
        
        return schedule_dict
    
    async def detect_substitutions(
        self,
        new_entries: list[ScheduleEntry],
        target_date: date
    ) -> list[Substitution]:
        """
        Detect substitutions by comparing new schedule with current schedule.
        
        Args:
            new_entries: List of newly parsed schedule entries
            target_date: Target date for substitutions
        
        Returns:
            List of detected Substitution objects
        """
        substitutions = []
        
        # Group entries by group name
        entries_by_group: dict[str, list[ScheduleEntry]] = {}
        for entry in new_entries:
            if entry.group_name not in entries_by_group:
                entries_by_group[entry.group_name] = []
            entries_by_group[entry.group_name].append(entry)
        
        # Process each group
        for group_name, entries in entries_by_group.items():
            # Get or create group
            group = await self.get_or_create_group(group_name)
            
            # Get current schedules
            current_schedules = await self.get_current_schedules(group.id)
            
            # Compare new entries with current schedules
            for entry in entries:
                key = f"{entry.day_of_week}_{entry.pair_number}_{entry.week_type}"
                current_schedule = current_schedules.get(key)
                
                if current_schedule is None:
                    # New schedule entry, create it
                    new_schedule = Schedule(
                        id=uuid.uuid4(),
                        group_id=group.id,
                        day_of_week=entry.day_of_week,
                        pair_number=entry.pair_number,
                        week_type=entry.week_type,
                        subject=entry.subject,
                        teacher=entry.teacher,
                        room=entry.room,
                    )
                    self.db_session.add(new_schedule)
                    await self.db_session.flush()
                    current_schedules[key] = new_schedule
                    continue
                
                # Check for changes (substitutions)
                subject_changed = (
                    (current_schedule.subject or "") != (entry.subject or "")
                )
                teacher_changed = (
                    (current_schedule.teacher or "") != (entry.teacher or "")
                )
                room_changed = (
                    (current_schedule.room or "") != (entry.room or "")
                )
                
                if subject_changed or teacher_changed or room_changed:
                    # Create substitution record
                    substitution = Substitution(
                        id=uuid.uuid4(),
                        schedule_id=current_schedule.id,
                        target_date=target_date,
                        new_subject=entry.subject,
                        new_teacher=entry.teacher,
                        new_room=entry.room,
                    )
                    self.db_session.add(substitution)
                    substitutions.append(substitution)
                    
                    # Update the schedule with new values
                    current_schedule.subject = entry.subject
                    current_schedule.teacher = entry.teacher
                    current_schedule.room = entry.room
            
            # Update or create schedules for new entries
            for entry in entries:
                key = f"{entry.day_of_week}_{entry.pair_number}_{entry.week_type}"
                if key not in current_schedules:
                    new_schedule = Schedule(
                        id=uuid.uuid4(),
                        group_id=group.id,
                        day_of_week=entry.day_of_week,
                        pair_number=entry.pair_number,
                        week_type=entry.week_type,
                        subject=entry.subject,
                        teacher=entry.teacher,
                        room=entry.room,
                    )
                    self.db_session.add(new_schedule)
        
        await self.db_session.flush()
        return substitutions
