"""Alembic environment configuration"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine

# Import your models and config
from app.database.connection import Base

# this is the Alembic Config object
config = context.config

# Get database URL from environment or config
# Try to get from environment first (for Railway)
import os
db_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url", ""))

# Remove asyncpg prefix if present and convert to psycopg2 format
if db_url:
    # Convert asyncpg URL to psycopg2 format for Alembic
    db_url = db_url.replace("+asyncpg", "").replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    if not db_url.startswith("postgresql"):
        # If no prefix, add psycopg2
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://")
    config.set_main_option("sqlalchemy.url", db_url)
else:
    # Fallback: try to import settings (may fail if env vars not set)
    try:
        from app.config import settings
        db_url = settings.database_url.replace("+asyncpg", "").replace("postgresql+asyncpg://", "postgresql+psycopg2://")
        config.set_main_option("sqlalchemy.url", db_url)
    except Exception:
        # If settings can't be loaded, use default from alembic.ini
        pass

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create sync engine for alembic
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = db_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
