"""
Database seeding utilities for the Golf League Management System.

This module provides functions for seeding the database with initial data,
particularly for creating administrative users and test data. All seeding
operations are designed to be idempotent and safe to run multiple times.
"""

import logging
from datetime import date
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database import SessionLocal
from app.models.user import AdminRole, MemberStatus, MemberType, User

# Configure logging
logger = logging.getLogger(__name__)

# Password hashing configuration for production security
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Minimum 12 rounds for security
)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with secure configuration.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Security:
        - Uses bcrypt with 12 rounds minimum
        - Automatically generates secure salt
        - Resistant to rainbow table attacks
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored password hash

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def admin_exists(db: Session) -> bool:
    """
    Check if an admin user already exists in the database.

    Args:
        db: Database session

    Returns:
        True if admin user exists, False otherwise
    """
    admin_user = db.query(User).filter(User.admin_roles == AdminRole.ADMIN).first()

    return admin_user is not None


def get_admin_user(db: Session) -> Optional[User]:
    """
    Get the admin user from the database.

    Args:
        db: Database session

    Returns:
        Admin User instance if exists, None otherwise
    """
    return db.query(User).filter(User.admin_roles == AdminRole.ADMIN).first()


def create_admin_user(
    db: Session,
    email: Optional[str] = None,
    password: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    force: bool = False,
) -> User:
    """
    Create an admin user in the database.

    Args:
        db: Database session
        email: Admin email (defaults to settings.admin_email)
        password: Admin password (defaults to settings.admin_password)
        first_name: Admin first name (defaults to settings.admin_first_name)
        last_name: Admin last name (defaults to settings.admin_last_name)
        force: If True, will update existing admin user

    Returns:
        Created or updated User instance

    Raises:
        ValueError: If admin already exists and force=False
        IntegrityError: If email constraint is violated
    """
    # Use settings defaults if not provided
    email = email or settings.admin_email
    password = password or settings.admin_password
    first_name = first_name or settings.admin_first_name
    last_name = last_name or settings.admin_last_name

    # Check if admin already exists
    existing_admin = get_admin_user(db)

    if existing_admin and not force:
        logger.warning(f"Admin user already exists: {existing_admin.email}")
        raise ValueError(
            f"Admin user already exists with email: {existing_admin.email}. "
            "Use force=True to update existing admin."
        )

    if existing_admin and force:
        logger.info(f"Updating existing admin user: {existing_admin.email}")
        # Update existing admin
        existing_admin.email = email
        existing_admin.password_hash = hash_password(password)
        existing_admin.first_name = first_name
        existing_admin.last_name = last_name

        try:
            db.commit()
            db.refresh(existing_admin)
            logger.info(f"Successfully updated admin user: {existing_admin.email}")
            return existing_admin
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Failed to update admin user: {e}")
            raise

    # Create new admin user
    logger.info(f"Creating new admin user: {email}")

    admin_user = User(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        member_status=MemberStatus.ACTIVE,
        member_type=MemberType.FULL,
        admin_roles=AdminRole.ADMIN,
        signup_date=date.today(),
    )

    try:
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info(f"Successfully created admin user: {admin_user.email}")
        return admin_user
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Failed to create admin user: {e}")
        raise


def seed_admin_user(
    email: Optional[str] = None,
    password: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    force: bool = False,
    dry_run: bool = False,
) -> Optional[User]:
    """
    Seed the database with an admin user (idempotent operation).

    This is the main entry point for admin user seeding. It handles
    database session management and provides comprehensive logging.

    Args:
        email: Admin email (defaults to settings.admin_email)
        password: Admin password (defaults to settings.admin_password)
        first_name: Admin first name (defaults to settings.admin_first_name)
        last_name: Admin last name (defaults to settings.admin_last_name)
        force: If True, will update existing admin user
        dry_run: If True, will only check if operation would succeed

    Returns:
        Created or updated User instance (None for dry_run)

    Raises:
        ValueError: If admin already exists and force=False
        Exception: For database connection or integrity errors
    """
    # Use settings defaults if not provided
    email = email or settings.admin_email
    password = password or settings.admin_password
    first_name = first_name or settings.admin_first_name
    last_name = last_name or settings.admin_last_name

    logger.info("Starting admin user seeding operation")
    logger.info(f"Target admin email: {email}")
    logger.info(f"Admin name: {first_name} {last_name}")
    logger.info(f"Force update: {force}")
    logger.info(f"Dry run: {dry_run}")

    # Create database session
    db = SessionLocal()

    try:
        # Check current state
        existing_admin = get_admin_user(db)

        if dry_run:
            if existing_admin:
                logger.info(f"DRY RUN: Admin user exists: {existing_admin.email}")
                if force:
                    logger.info("DRY RUN: Would update existing admin user")
                else:
                    logger.info("DRY RUN: Would skip (admin exists, force=False)")
            else:
                logger.info("DRY RUN: Would create new admin user")
            return None

        # Perform the seeding operation
        admin_user = create_admin_user(
            db=db,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            force=force,
        )

        logger.info("Admin user seeding completed successfully")
        return admin_user

    except Exception as e:
        logger.error(f"Admin user seeding failed: {e}")
        raise
    finally:
        db.close()


def validate_admin_credentials(email: str, password: str) -> bool:
    """
    Validate admin credentials against the database.

    Args:
        email: Admin email to validate
        password: Plain text password to validate

    Returns:
        True if credentials are valid, False otherwise
    """
    db = SessionLocal()

    try:
        admin_user = (
            db.query(User)
            .filter(User.email == email, User.admin_roles == AdminRole.ADMIN)
            .first()
        )

        if not admin_user:
            logger.warning(f"Admin user not found: {email}")
            return False

        is_valid = verify_password(password, admin_user.password_hash)

        if is_valid:
            logger.info(f"Admin credentials validated successfully: {email}")
        else:
            logger.warning(f"Invalid password for admin user: {email}")

        return is_valid

    except Exception as e:
        logger.error(f"Failed to validate admin credentials: {e}")
        return False
    finally:
        db.close()
