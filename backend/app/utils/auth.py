"""
Authentication utilities for JWT token management.

This module provides JWT token creation, validation, and user authentication
functions for the Golf League Management System API.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.user import User

# Password context for hashing and verification (consistent with seeding module)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Match seeding module configuration
)


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


def get_password_hash(password: str) -> str:
    """
    Hash a password for storage.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> Union[User, None]:
    """
    Authenticate a user by email and password with account lockout protection.

    Args:
        db: Database session
        email: User email address
        password: Plain text password

    Returns:
        User instance if authentication successful, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    # Check if account is locked
    if user.is_locked:
        return None

    # Check if user is active
    if not user.is_active:
        return None

    # Verify password
    if not verify_password(password, user.password_hash):
        # Increment failed attempts and potentially lock account
        user.increment_failed_attempts()
        db.commit()
        return None

    # Successful login - reset failed attempts
    user.reset_failed_attempts()
    db.commit()

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        data: Data to encode in the token

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()

    # Refresh tokens last 7 days
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def get_user_from_token(db: Session, token: str) -> Optional[User]:
    """
    Get user from a JWT token.

    Args:
        db: Database session
        token: JWT token string

    Returns:
        User instance if token is valid and user exists, None otherwise
    """
    payload = verify_token(token)

    if payload is None:
        return None

    email: str = payload.get("sub")
    if email is None:
        return None

    user = db.query(User).filter(User.email == email).first()
    return user