"""
Database connection and session management for Golf League Management System.

This module provides SQLAlchemy 2.x database connection, session management,
and base model configuration for the application.
"""

from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

# Create synchronous database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=settings.debug  # Log SQL queries in debug mode
)

# Create session factory for synchronous operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base for model definitions
Base = declarative_base()

# For future async operations (optional, but good to have ready)
# async_engine = create_async_engine(
#     settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
#     pool_pre_ping=True,
#     pool_recycle=300,
#     echo=settings.debug
# )
#
# AsyncSessionLocal = async_sessionmaker(
#     async_engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session for FastAPI endpoints.

    Yields:
        Session: SQLAlchemy database session

    Example:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """
    Test database connection.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def create_tables() -> None:
    """
    Create all tables defined in models.

    Note: In production, use Alembic migrations instead of this function.
    This is primarily for testing and development setup.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """
    Drop all tables defined in models.

    Warning: This will delete all data! Use with caution.
    """
    Base.metadata.drop_all(bind=engine)