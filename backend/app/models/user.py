"""
User model for Golf League Management System.

This module defines the User model that represents golf league members
with their profile information, membership details, and administrative roles.
Supports complete member lifecycle management including signup, status changes,
and financial tracking.
"""

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (DECIMAL, Boolean, CheckConstraint, Date, DateTime,
                        Enum, Index, String, Text, func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MemberStatus(str, enum.Enum):
    """Member status enumeration for golf league members."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class MemberType(str, enum.Enum):
    """Member type enumeration for different membership levels."""

    CANDIDATE = "candidate"
    FULL = "full"
    LIFETIME = "lifetime"


class AdminRole(str, enum.Enum):
    """Administrative role enumeration for member permissions."""

    ADMIN = "admin"
    TREASURER = "treasurer"
    COURSE_COORDINATOR = "course_coordinator"
    TOURNAMENT_COORDINATOR = "tournament_coordinator"


class User(Base):
    """
    User model representing golf league members.

    This model stores all member information including profile data,
    membership status, administrative roles, financial balance, and
    golf-specific information like GHIN ID and AGA membership.

    Attributes:
        member_id: Primary key UUID for the member
        email: Unique email address for login and communication
        password_hash: Hashed password for authentication
        first_name: Member's first name
        last_name: Member's last name
        phone_number: Optional contact phone number
        date_of_birth: Optional birth date (used for tee eligibility)
        member_status: Current membership status (active/inactive)
        member_type: Type of membership (candidate/full/lifetime)
        admin_roles: Optional administrative role for permissions
        GHIN_id: Golf Handicap and Information Network ID
        member_balance: Current account balance for fees and prizes
        signup_date: Date when member joined the league
        AGA_membership_expiry: American Golf Association membership expiry
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated

    Business Rules:
        - Email must be unique across all members
        - Member balance cannot go below -$500 (credit limit)
        - GHIN ID must be unique if provided
        - Member status determines participation eligibility
        - Admin roles grant specific system permissions
        - Date of birth determines forward/senior tee eligibility
    """

    __tablename__ = "users"

    # Primary key
    member_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Primary key UUID for the member",
    )

    # Authentication fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique email address for login and communication",
    )

    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, doc="Hashed password for authentication"
    )

    # Profile information
    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="Member's first name"
    )

    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False, doc="Member's last name"
    )

    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, doc="Optional contact phone number"
    )

    date_of_birth: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        doc="Optional birth date (used for forward and 75+ tee eligibility)",
    )

    # Membership information
    member_status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus),
        nullable=False,
        default=MemberStatus.ACTIVE,
        index=True,
        doc="Current membership status (active/inactive)",
    )

    member_type: Mapped[MemberType] = mapped_column(
        Enum(MemberType),
        nullable=False,
        default=MemberType.CANDIDATE,
        index=True,
        doc="Type of membership (candidate/full/lifetime)",
    )

    admin_roles: Mapped[Optional[AdminRole]] = mapped_column(
        Enum(AdminRole),
        nullable=True,
        doc="Optional administrative role for permissions",
    )

    # Golf-specific information
    GHIN_id: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        unique=True,
        index=True,
        doc="Golf Handicap and Information Network ID",
    )

    # Financial information
    member_balance: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
        default=Decimal("0.00"),
        doc="Current account balance for fees and prizes",
    )

    # Important dates
    signup_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=func.current_date(),
        doc="Date when member joined the league",
    )

    AGA_membership_expiry: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, doc="American Golf Association membership expiry date"
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        doc="Timestamp when record was created",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        doc="Timestamp when record was last updated",
    )

    # Security fields for account lockout
    failed_login_attempts: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        doc="Number of consecutive failed login attempts",
    )

    locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Account lockout expiration time (null if not locked)",
    )

    # Table constraints
    __table_args__ = (
        # Business rule: Member balance cannot go below -$500 (credit limit)
        CheckConstraint("member_balance >= -500.00", name="check_member_balance_limit"),
        # Performance indexes for common queries
        Index("idx_users_email", "email"),
        Index("idx_users_member_status", "member_status"),
        Index("idx_users_member_type", "member_type"),
        Index("idx_users_GHIN_id", "GHIN_id"),
        Index("idx_users_signup_date", "signup_date"),
        Index("idx_users_created_at", "created_at"),
        # Composite indexes for common query patterns
        Index("idx_users_status_type", "member_status", "member_type"),
        Index("idx_users_name_search", "last_name", "first_name"),
    )

    def __repr__(self) -> str:
        """String representation of User instance."""
        return (
            f"<User(member_id='{self.member_id}', "
            f"email='{self.email}', "
            f"name='{self.first_name} {self.last_name}', "
            f"status='{self.member_status}', "
            f"type='{self.member_type}')>"
        )

    @property
    def full_name(self) -> str:
        """Get member's full name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        """Check if member is currently active."""
        return self.member_status == MemberStatus.ACTIVE

    @property
    def is_admin(self) -> bool:
        """Check if member has any administrative role."""
        # Import here to avoid circular imports
        from app.api.dependencies import get_user_roles

        user_roles = get_user_roles(self)
        return len(user_roles) > 0

    @property
    def can_participate(self) -> bool:
        """Check if member can participate in tournaments."""
        return self.member_status == MemberStatus.ACTIVE and self.member_type in [
            MemberType.FULL,
            MemberType.LIFETIME,
        ]

    @property
    def is_senior_eligible(self) -> bool:
        """Check if member is eligible for senior/75+ tees (age 75+)."""
        if not self.date_of_birth:
            return False

        from datetime import date

        today = date.today()
        age = today.year - self.date_of_birth.year

        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        ):
            age -= 1

        return age >= 75

    @property
    def balance_status(self) -> str:
        """Get member's balance status description."""
        if self.member_balance >= 0:
            return "Credit"
        elif self.member_balance >= -100:
            return "Minor Debit"
        elif self.member_balance >= -300:
            return "Significant Debit"
        else:
            return "Critical Debit"

    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if not self.locked_until:
            return False

        from datetime import datetime, timezone
        return datetime.now(timezone.utc) < self.locked_until

    def reset_failed_attempts(self) -> None:
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0
        self.locked_until = None

    def increment_failed_attempts(self) -> None:
        """Increment failed login attempts and lock if threshold reached."""
        self.failed_login_attempts += 1

        # Lock account after 5 failed attempts for 15 minutes
        if self.failed_login_attempts >= 5:
            from datetime import datetime, timezone, timedelta
            self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
