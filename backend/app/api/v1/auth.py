"""
Authentication API endpoints.

This module provides JWT-based authentication endpoints including login,
logout, token refresh, and user information retrieval.
"""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.settings import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    ErrorResponse,
    LoginRequest,
    LogoutResponse,
    PasswordChangeRequest,
    PasswordChangeResponse,
    Token,
    TokenRefresh,
    UserInfo,
)
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user with email and password, return JWT tokens.",
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def login(
    login_data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """
    Authenticate user and return access and refresh tokens.

    This endpoint validates user credentials and returns JWT tokens
    for accessing protected endpoints.

    Args:
        login_data: User login credentials (email and password)
        db: Database session

    Returns:
        JWT access and refresh tokens with expiration information

    Raises:
        HTTPException: If credentials are invalid or user is inactive
    """
    user = authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create token data
    token_data = {"sub": user.email, "user_id": str(user.member_id)}

    # Generate tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Token",
    description="Use refresh token to get new access token.",
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired refresh token"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def refresh_token(
    token_data: TokenRefresh,
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """
    Refresh an access token using a valid refresh token.

    This endpoint allows clients to obtain a new access token
    without requiring the user to log in again.

    Args:
        token_data: Refresh token data
        db: Database session

    Returns:
        New JWT access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid or expired
    """
    # Verify refresh token
    payload = verify_token(token_data.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user email from token
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user still exists and is active
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new token data
    new_token_data = {"sub": user.email, "user_id": str(user.member_id)}

    # Generate new tokens
    access_token = create_access_token(new_token_data)
    refresh_token = create_refresh_token(new_token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="User Logout",
    description="Logout current user (client should discard tokens).",
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
) -> LogoutResponse:
    """
    Logout the current authenticated user.

    Note: This endpoint primarily serves to validate the user is authenticated
    and provides a logout timestamp. In a stateless JWT implementation,
    actual token invalidation should be handled client-side by discarding tokens.

    For production systems, consider implementing token blacklisting
    or shorter token expiration times for better security.

    Args:
        current_user: Current authenticated user

    Returns:
        Logout confirmation with timestamp
    """
    return LogoutResponse(
        message=f"Successfully logged out user: {current_user.email}",
        logged_out_at=datetime.now(timezone.utc),
    )


@router.get(
    "/me",
    response_model=UserInfo,
    status_code=status.HTTP_200_OK,
    summary="Current User Info",
    description="Get information about the currently authenticated user.",
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserInfo:
    """
    Get information about the currently authenticated user.

    This endpoint returns comprehensive information about the authenticated
    user including profile data, membership status, and account details.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user information
    """
    return UserInfo(
        member_id=current_user.member_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        full_name=current_user.full_name,
        member_status=current_user.member_status.value,
        member_type=current_user.member_type.value,
        admin_roles=current_user.admin_roles.value if current_user.admin_roles else None,
        is_admin=current_user.is_admin,
        member_balance=float(current_user.member_balance),
        signup_date=current_user.signup_date,
        created_at=current_user.created_at,
    )


@router.post(
    "/change-password",
    response_model=PasswordChangeResponse,
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="Change user password with current password verification.",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid current password or validation error"},
        401: {"model": ErrorResponse, "description": "Not authenticated"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PasswordChangeResponse:
    """
    Change the password for the currently authenticated user.

    This endpoint allows authenticated users to change their password
    by providing their current password and a new password that meets
    security requirements.

    Args:
        password_data: Password change request data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Password change confirmation with timestamp

    Raises:
        HTTPException: If current password is invalid or validation fails
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Hash the new password
    new_password_hash = get_password_hash(password_data.new_password)

    # Update user password
    current_user.password_hash = new_password_hash
    current_user.updated_at = datetime.now(timezone.utc)

    # Commit changes
    db.commit()
    db.refresh(current_user)

    return PasswordChangeResponse(
        message="Password changed successfully",
        changed_at=datetime.now(timezone.utc),
    )