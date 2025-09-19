"""
Models package for Golf League Management System.

This package contains all SQLAlchemy model definitions for the application.
Models are organized by domain and include proper relationships, constraints,
and business logic validation.
"""

from .user import User

__all__ = ["User"]
