"""
FastAPI dependencies for authentication and authorization.

This module provides dependency functions for securing API endpoints
and managing authentication state, including role-based access control.
"""

from typing import Callable
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, AdminRole
from app.utils.auth import get_user_from_token

# OAuth2 scheme for JWT token authentication
security = HTTPBearer()


def get_user_roles(user: User) -> set[AdminRole]:
    """
    Return set of all roles user has (including inherited ones).

    Role inheritance logic:
    - If user has AdminRole.ADMIN, they inherit ALL other admin roles
    - Other roles (TREASURER, COURSE_COORDINATOR, TOURNAMENT_COORDINATOR) only have their specific permissions
    - Regular members (admin_roles = None) have no admin roles

    Args:
        user: User instance to check roles for

    Returns:
        Set of AdminRole enums that the user has access to
    """
    if user.admin_roles is None:
        # Regular member with no admin roles
        return set()

    if user.admin_roles == AdminRole.ADMIN:
        # Admin inherits all roles
        return set(AdminRole)

    # Return the specific role they have
    return {user.admin_roles}


def require_roles(*required_roles: AdminRole) -> Callable[[User], User]:
    """
    Dependency factory requiring any of the specified roles.

    This creates a dependency function that checks if the current user
    has any of the required roles (including inherited roles from admin).

    Args:
        *required_roles: One or more AdminRole enums that are acceptable

    Returns:
        Dependency function that validates user roles

    Raises:
        HTTPException: If user doesn't have any of the required roles

    Example:
        # Require admin role only
        @app.get("/admin-only")
        def admin_endpoint(user: User = Depends(require_roles(AdminRole.ADMIN))):
            pass

        # Require either treasurer or admin role
        @app.get("/financial")
        def financial_endpoint(user: User = Depends(require_roles(AdminRole.TREASURER, AdminRole.ADMIN))):
            pass
    """
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        # If no roles are required, allow anyone authenticated
        if not required_roles:
            return current_user

        user_roles = get_user_roles(current_user)

        # Check if user has any of the required roles
        if not user_roles.intersection(set(required_roles)):
            # Create user-friendly error message
            if len(required_roles) == 1:
                role_name = required_roles[0].value.replace('_', ' ').title()
                detail = f"Access denied. This endpoint requires {role_name} role."
            else:
                role_names = [role.value.replace('_', ' ').title() for role in required_roles]
                detail = f"Access denied. This endpoint requires one of the following roles: {', '.join(role_names)}."

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail,
            )

        return current_user

    return role_dependency


def require_member_self_or_admin(member_id: UUID) -> Callable[[User], User]:
    """
    Dependency factory requiring user to be accessing their own data OR be an admin.

    This dependency allows two access patterns:
    1. Member accessing their own data (current_user.member_id == member_id)
    2. Admin accessing any member's data (any admin role)

    Args:
        member_id: UUID of the member whose data is being accessed

    Returns:
        Dependency function that validates self-access or admin privileges

    Raises:
        HTTPException: 403 if user is neither the member nor an admin

    Example Usage:
        @router.get("/members/{member_id}/details")
        def get_member_details(
            member_id: UUID = Path(...),
            current_user: User = Depends(require_member_self_or_admin(member_id))
        ):
            # current_user is guaranteed to be member_id owner OR admin
            return member_details
    """
    def self_or_admin_dependency(current_user: User = Depends(get_current_user)) -> User:
        # Check if user is accessing their own data
        if current_user.member_id == member_id:
            return current_user

        # Check if user has admin privileges
        user_roles = get_user_roles(current_user)
        if user_roles:  # If user has any admin roles, allow access
            return current_user

        # Access denied - neither self nor admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your own data unless you have administrative privileges.",
        )

    return self_or_admin_dependency


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    token = credentials.credentials
    user = get_user_from_token(db, token)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    return user




def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User | None:
    """
    Get the current user if authenticated, otherwise return None.

    This dependency allows endpoints to be accessed by both authenticated
    and anonymous users, with different behavior based on authentication status.

    Args:
        credentials: HTTP Bearer token credentials (optional)
        db: Database session

    Returns:
        Current authenticated user or None
    """
    if not credentials:
        return None

    token = credentials.credentials
    user = get_user_from_token(db, token)

    if user and user.is_active:
        return user

    return None


# Convenience dependencies for common role patterns
def require_admin() -> Callable[[User], User]:
    """Convenience dependency requiring ADMIN role only."""
    return require_roles(AdminRole.ADMIN)


def require_financial_access() -> Callable[[User], User]:
    """Convenience dependency requiring TREASURER or ADMIN role for financial operations."""
    return require_roles(AdminRole.TREASURER, AdminRole.ADMIN)


def require_any_admin() -> Callable[[User], User]:
    """Convenience dependency requiring any administrative role."""
    return require_roles(*AdminRole)