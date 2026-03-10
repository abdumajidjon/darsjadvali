"""Database models"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
import uuid

# Base class for models (moved here to avoid circular import in Alembic)
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column("telegram_id", Integer, unique=True, nullable=False, index=True)
    group_id = Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    role = Column("role", String(20), default="student")
    language = Column("language", String(5), default="uz")
    
    group = relationship("Group", back_populates="users")


class Group(Base):
    """Group model"""
    __tablename__ = "groups"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String(50), unique=True, nullable=False, index=True)
    
    users = relationship("User", back_populates="group")
    schedules = relationship("Schedule", back_populates="group", cascade="all, delete-orphan")


class Schedule(Base):
    """Schedule model"""
    __tablename__ = "schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False, index=True)
    day_of_week = Column("day_of_week", Integer, nullable=False)  # 0=Monday, 6=Sunday
    pair_number = Column("pair_number", Integer, nullable=False)  # 1, 2, 3 (I, II, III)
    week_type = Column("week_type", String(10), nullable=False)  # ODD or EVEN
    subject = Column("subject", String(255), nullable=True)
    teacher = Column("teacher", String(255), nullable=True)
    room = Column("room", String(50), nullable=True)
    
    group = relationship("Group", back_populates="schedules")
    substitutions = relationship("Substitution", back_populates="schedule", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("group_id", "day_of_week", "pair_number", "week_type", name="uq_schedule"),
    )


class Substitution(Base):
    """Substitution model"""
    __tablename__ = "substitutions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column("schedule_id", UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False, index=True)
    target_date = Column("target_date", Date, nullable=False, index=True)
    new_subject = Column("new_subject", String(255), nullable=True)
    new_teacher = Column("new_teacher", String(255), nullable=True)
    new_room = Column("new_room", String(50), nullable=True)
    
    schedule = relationship("Schedule", back_populates="substitutions")
