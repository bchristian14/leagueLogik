"""
Authentication-related Pydantic schemas.

This module contains all Pydantic models for authentication API
request and response serialization.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, Field, validator


class LoginRequest(BaseModel):
    """Request schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=100, description="User password"
    )


class PasswordChangeRequest(BaseModel):
    """Request schema for password change."""

    current_password: str = Field(..., description="Current user password")
    new_password: str = Field(
        ..., min_length=8, max_length=100, description="New password"
    )
    confirm_password: str = Field(..., description="Confirm new password")

    @validator("new_password")
    def validate_password_strength(cls, v):
        """Validate password strength requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if len(v) > 100:
            raise ValueError("Password must not exceed 100 characters")

        # Check for at least one uppercase letter
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        # Check for at least one lowercase letter
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        # Check for at least one digit
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")

        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class PasswordChangeResponse(BaseModel):
    """Response schema for successful password change."""

    message: str = Field(default="Password changed successfully", description="Success message")
    changed_at: datetime = Field(..., description="Password change timestamp")


class Token(BaseModel):
    """Response schema for token information."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenRefresh(BaseModel):
    """Request schema for token refresh."""

    refresh_token: str = Field(..., description="JWT refresh token")


class UserInfo(BaseModel):
    """Response schema for current user information."""

    member_id: UUID = Field(..., description="User member ID")
    email: str = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    full_name: str = Field(..., description="User full name")
    member_status: str = Field(..., description="Member status")
    member_type: str = Field(..., description="Member type")
    admin_roles: Optional[str] = Field(None, description="Admin role if applicable")
    is_admin: bool = Field(..., description="Whether user has admin privileges")
    member_balance: float = Field(..., description="Current member balance")
    signup_date: datetime = Field(..., description="Date when member joined")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class LogoutResponse(BaseModel):
    """Response schema for successful logout."""

    message: str = Field(default="Successfully logged out", description="Logout message")
    logged_out_at: datetime = Field(..., description="Logout timestamp")


class ErrorResponse(BaseModel):
    """Response schema for authentication errors."""

    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Specific error code")