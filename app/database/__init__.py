"""Database package"""

# Lazy imports to avoid loading connection.py during Alembic migrations
def _get_connection():
    """Lazy import connection module"""
    from .connection import get_db_session, init_db
    return get_db_session, init_db

def _get_models():
    """Lazy import models"""
    from .models import User, Group, Schedule, Substitution
    return User, Group, Schedule, Substitution

# Export functions for lazy access
def get_db_session():
    """Get database session"""
    from .connection import get_db_session as _get_db_session
    return _get_db_session

def init_db():
    """Initialize database"""
    from .connection import init_db as _init_db
    return _init_db

# Direct imports for convenience (but these will trigger connection.py import)
try:
    from .models import User, Group, Schedule, Substitution
except ImportError:
    # During Alembic migrations, this might fail
    User = Group = Schedule = Substitution = None

__all__ = [
    "get_db_session",
    "init_db",
    "User",
    "Group",
    "Schedule",
    "Substitution",
]
