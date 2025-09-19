# Role-Based Access Control Patterns

*Created: 2025-09-19 | Implementation: T123 Core Role System + T123.7 Member Self-Access*

## Overview

This document provides comprehensive guidance for implementing role-based access control (RBAC) in the LeagueLogik golf league management system. The role system provides flexible, extensible permission management using FastAPI dependency injection patterns.

## Role Hierarchy

### Admin Roles (AdminRole Enum)
- **ADMIN**: Full system access, inherits all other admin roles
- **TREASURER**: Financial management (transactions, member balances)
- **COURSE_COORDINATOR**: Course and venue management
- **TOURNAMENT_COORDINATOR**: Tournament setup and scoring management

### Access Levels
1. **Public**: No authentication required
2. **Member**: Any authenticated user
3. **Admin**: Users with any admin role
4. **Role-Specific**: Users with specific admin roles
5. **Self-Access**: Members accessing own data OR admin accessing any data (T123.7)

## Core Functions

### `get_user_roles(user: User) -> set[AdminRole]`

Returns the set of all roles a user has, including inherited roles.

**Role Inheritance Logic:**
- `AdminRole.ADMIN` → Inherits ALL other admin roles
- Other admin roles → Only their specific permissions
- Regular members → Empty set (no admin roles)

```python
# Usage examples
user_roles = get_user_roles(current_user)

# Check for specific role
if AdminRole.ADMIN in user_roles:
    # User has admin access

if AdminRole.TREASURER in user_roles:
    # User has financial access (treasurer or admin)

# Check for any admin role (used in self-access patterns)
if user_roles:  # Empty set = no admin roles
    # User has administrative privileges
```

### `require_roles(*required_roles: AdminRole) -> Callable[[User], User]`

Dependency factory that creates role-checking dependencies for endpoints.

**Logic:** User needs ANY of the specified roles (OR logic)

```python
# Single role requirement
@router.get("/admin-panel")
def admin_panel(user: User = Depends(require_roles(AdminRole.ADMIN))):
    return {"message": "Admin access granted"}

# Multiple role options (OR logic)
@router.get("/financial-data")
def financial_data(user: User = Depends(require_roles(AdminRole.TREASURER, AdminRole.ADMIN))):
    return {"data": "financial_information"}

# Any admin role
@router.get("/admin-tools")
def admin_tools(user: User = Depends(require_roles(*AdminRole))):
    return {"tools": "admin_tools"}
```

## Convenience Dependencies

Pre-built dependencies for common access patterns:

### `require_admin()`
Requires ADMIN role only (highest privilege level).

```python
@router.post("/members")
def create_member(user: User = Depends(require_admin())):
    # Only full admins can create members
    pass
```

### `require_financial_access()`
Requires TREASURER or ADMIN role for financial operations.

```python
@router.post("/transactions")
def create_transaction(user: User = Depends(require_financial_access())):
    # Treasurers and admins can create transactions
    pass
```

### `require_any_admin()`
Requires any administrative role.

```python
@router.get("/admin-dashboard")
def admin_dashboard(user: User = Depends(require_any_admin())):
    # Any admin role can access dashboard
    pass
```

### `require_member_self_or_admin(member_id: UUID)`
Dependency factory for member self-access or admin override patterns.

**Access Logic:**
1. **Self-Access**: `current_user.member_id == member_id`
2. **Admin Override**: User has any admin role

```python
@router.get("/members/{member_id}/details")
def get_member_details(
    member_id: UUID = Path(...),
    current_user: User = Depends(require_member_self_or_admin(member_id)),
    db: Session = Depends(get_db)
):
    # current_user is guaranteed to be member_id owner OR admin
    return get_member_by_id(db, member_id)

@router.get("/members/{member_id}/transactions")
def get_member_transactions(
    member_id: UUID = Path(...),
    current_user: User = Depends(require_member_self_or_admin(member_id))
):
    # Member can view own transactions, admin can view any
    return {"transactions": []}
```

## Implementation Patterns

### Pattern 1: Public Access
No dependency required for public endpoints.

```python
@router.get("/tournament-schedule")
def public_tournament_schedule():
    # Anyone can view tournament schedule
    return {"tournaments": []}
```

### Pattern 2: Authenticated Member Access
Any authenticated user (members or admins).

```python
@router.get("/my-profile")
def get_my_profile(user: User = Depends(get_current_user)):
    # Any authenticated user can view their profile
    return {"profile": user}
```

### Pattern 3: Admin-Only Access
Requires any admin role.

```python
@router.get("/all-members")
def list_all_members(user: User = Depends(require_any_admin())):
    # Only admins can view all members
    return {"members": []}
```

### Pattern 4: Role-Specific Access
Requires specific admin role(s).

```python
@router.get("/financial-reports")
def financial_reports(user: User = Depends(require_financial_access())):
    # Only treasurers and admins can view financial reports
    return {"reports": []}
```

### Pattern 5: Member Self-Access or Admin
Members can access their own data, admins can access any member data.

**Key Features:**
- **Path Parameter Integration**: Uses FastAPI Path parameter for member_id
- **Self-Access Logic**: Compares `current_user.member_id` with path `member_id`
- **Admin Override**: Any admin role grants access to any member data
- **Security**: 403 Forbidden with clear message if neither condition met

```python
from uuid import UUID
from fastapi import Path, Depends

@router.get("/members/{member_id}")
def get_member_details(
    member_id: UUID = Path(..., description="Member ID to retrieve"),
    current_user: User = Depends(require_member_self_or_admin(member_id)),
    db: Session = Depends(get_db)
):
    # current_user is pre-authorized to access member_id data
    member = get_member_by_id(db, member_id)
    return {"member": member}

@router.put("/members/{member_id}")
def update_member_profile(
    member_id: UUID = Path(...),
    member_update: MemberUpdate,
    current_user: User = Depends(require_member_self_or_admin(member_id))
):
    # Member can update own profile, admin can update any profile
    return update_member(db, member_id, member_update)

@router.get("/members/{member_id}/transactions")
def get_member_transactions(
    member_id: UUID = Path(...),
    current_user: User = Depends(require_member_self_or_admin(member_id))
):
    # Financial data access with self-access + admin override
    return {"transactions": get_transactions_for_member(member_id)}

@router.get("/members/{member_id}/balance")
def get_member_balance(
    member_id: UUID = Path(...),
    current_user: User = Depends(require_member_self_or_admin(member_id))
):
    # Balance information - sensitive data with proper access control
    return {"balance": get_current_balance(member_id)}
```

## Error Handling

The role system provides user-friendly error messages:

### Single Role Error
```
HTTP 403 Forbidden
{
  "detail": "Access denied. This endpoint requires Admin role."
}
```

### Multiple Role Error
```
HTTP 403 Forbidden
{
  "detail": "Access denied. This endpoint requires one of the following roles: Treasurer, Admin."
}
```

### Self-Access Denied Error
```
HTTP 403 Forbidden
{
  "detail": "Access denied. You can only access your own data unless you have administrative privileges."
}
```

## Testing Patterns

### Unit Test Structure
```python
def test_require_roles_admin_access():
    """Test that admin role grants access to admin-only endpoint."""
    admin_user = create_user_with_role(AdminRole.ADMIN)
    dependency = require_roles(AdminRole.ADMIN)
    result = dependency(admin_user)
    assert result == admin_user

def test_require_roles_insufficient_permissions():
    """Test that insufficient permissions raise 403."""
    member_user = create_user_with_role(None)  # Regular member
    dependency = require_roles(AdminRole.ADMIN)

    with pytest.raises(HTTPException) as exc_info:
        dependency(member_user)

    assert exc_info.value.status_code == 403
    assert "Admin role" in exc_info.value.detail
```

### Integration Test Structure
```python
def test_admin_endpoint_access(client, admin_token):
    """Test admin endpoint with proper authentication."""
    response = client.get(
        "/api/v1/admin-only-endpoint",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_admin_endpoint_denied(client, member_token):
    """Test admin endpoint denies member access."""
    response = client.get(
        "/api/v1/admin-only-endpoint",
        headers={"Authorization": f"Bearer {member_token}"}
    )
    assert response.status_code == 403
```

### Member Self-Access Test Structure
```python
def test_member_self_access_success():
    """Test member can access their own data."""
    member_user = create_user_with_member_id()
    dependency = require_member_self_or_admin(member_user.member_id)
    result = dependency(member_user)
    assert result == member_user

def test_admin_can_access_any_member():
    """Test admin can access any member's data."""
    admin_user = create_user_with_role(AdminRole.ADMIN)
    other_member_id = uuid4()
    dependency = require_member_self_or_admin(other_member_id)
    result = dependency(admin_user)
    assert result == admin_user

def test_member_cannot_access_other_member():
    """Test member cannot access another member's data."""
    member_user = create_user_with_member_id()
    other_member_id = uuid4()  # Different member ID
    dependency = require_member_self_or_admin(other_member_id)

    with pytest.raises(HTTPException) as exc_info:
        dependency(member_user)

    assert exc_info.value.status_code == 403
    assert "your own data" in exc_info.value.detail

def test_self_access_integration(client, member_tokens):
    """Integration test for member self-access endpoints."""
    member_id, token = member_tokens['member1']

    # Member can access own data
    response = client.get(
        f"/api/v1/members/{member_id}/transactions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Member cannot access other member's data
    other_member_id = member_tokens['member2'][0]
    response = client.get(
        f"/api/v1/members/{other_member_id}/transactions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_admin_override_integration(client, admin_token, member_tokens):
    """Integration test for admin override on member endpoints."""
    member_id = member_tokens['member1'][0]

    # Admin can access any member's data
    response = client.get(
        f"/api/v1/members/{member_id}/transactions",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
```

## Migration Guide

### From Legacy Boolean Admin Check

**Before (Legacy):**
```python
def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(403, "Not enough permissions")
    return current_user

@router.get("/admin-endpoint")
def admin_endpoint(user: User = Depends(get_current_admin)):
    pass
```

**After (Role-Based):**
```python
@router.get("/admin-endpoint")
def admin_endpoint(user: User = Depends(require_any_admin())):
    pass
```

### For Specific Role Requirements

**Financial Endpoints:**
```python
# Old: Generic admin check
@router.get("/transactions")
def get_transactions(user: User = Depends(get_current_admin)):
    pass

# New: Specific role requirement
@router.get("/transactions")
def get_transactions(user: User = Depends(require_financial_access())):
    pass
```

## Best Practices

### 1. Use Specific Role Dependencies
Prefer specific role requirements over generic admin checks:
```python
# Good: Specific requirement
require_financial_access()

# Less ideal: Generic requirement
require_any_admin()
```

### 2. Descriptive Endpoint Protection
Make role requirements clear in endpoint design:
```python
@router.post("/members", dependencies=[Depends(require_admin())])
def create_member(member_data: MemberCreate):
    # Role requirement is explicit in decorator
    pass
```

### 3. Consistent Error Messages
Let the role system handle error messages rather than custom ones:
```python
# Good: Let require_roles() handle the error
def admin_endpoint(user: User = Depends(require_admin())):
    pass

# Avoid: Custom error handling
def admin_endpoint(user: User = Depends(get_current_user)):
    if AdminRole.ADMIN not in get_user_roles(user):
        raise HTTPException(403, "Custom error")  # Inconsistent
```

### 4. Role Checking in Business Logic
For complex authorization logic, use `get_user_roles()`:
```python
def process_member_data(user: User, target_member_id: UUID):
    user_roles = get_user_roles(user)

    # Member can only modify own data
    if not user_roles and user.member_id != target_member_id:
        raise HTTPException(403, "Can only modify your own data")

    # Admins can modify any data
    # Continue processing...

# Better approach: Use require_member_self_or_admin dependency
@router.put("/members/{member_id}/profile")
def update_member_profile(
    member_id: UUID = Path(...),
    profile_data: MemberProfileUpdate,
    current_user: User = Depends(require_member_self_or_admin(member_id))
):
    # Access control handled by dependency, focus on business logic
    return update_profile(member_id, profile_data)
```

## Future Extensions

### Upcoming Integration (T211 & T321)
The member self-access pattern is designed for immediate integration with:

**T211 Member Management Endpoints:**
- `GET /members/{member_id}` - Member profile access
- `PUT /members/{member_id}` - Profile updates
- `GET /members/{member_id}/status` - Membership status

**T321 Financial Management Endpoints:**
- `GET /members/{member_id}/transactions` - Transaction history
- `GET /members/{member_id}/balance` - Current balance
- `POST /members/{member_id}/transactions` - Add transactions (admin only)

### Adding New Roles
1. Add to `AdminRole` enum in `app/models/user.py`
2. Update role inheritance logic if needed
3. Create convenience dependencies as needed
4. Add tests for new role combinations

### Extending Self-Access Patterns
The `require_member_self_or_admin` pattern can be extended for other resources:

```python
def require_tournament_participant_or_admin(tournament_id: UUID):
    """Allow tournament participants or admins to access tournament data."""
    def dependency(current_user: User = Depends(get_current_user)):
        # Check if user is participating in tournament
        if is_tournament_participant(current_user.member_id, tournament_id):
            return current_user

        # Check admin privileges
        user_roles = get_user_roles(current_user)
        if AdminRole.TOURNAMENT_COORDINATOR in user_roles or AdminRole.ADMIN in user_roles:
            return current_user

        raise HTTPException(403, "Access denied. Tournament participants and coordinators only.")
    return dependency
```

### Complex Permission Logic
For advanced scenarios, create custom dependency functions:
```python
def require_tournament_access():
    """Custom dependency for tournament-specific access."""
    def dependency(current_user: User = Depends(get_current_user)):
        user_roles = get_user_roles(current_user)

        # Complex logic here
        if AdminRole.TOURNAMENT_COORDINATOR in user_roles:
            return current_user
        if AdminRole.ADMIN in user_roles:
            return current_user
        # Additional custom logic...

        raise HTTPException(403, "Tournament access denied")

    return dependency
```

## Related Documentation

- **User Model**: `app/models/user.py` - AdminRole enum and User model
- **Dependencies**: `app/api/dependencies.py` - Core role system implementation
- **Tests**: `tests/test_role_system.py` - Comprehensive test suite
- **Authentication**: `app/api/v1/auth.py` - Authentication endpoints
- **Development Roadmap**: `docs/development_roadmap.md` - T123 task series

---

*This documentation reflects the complete T123 role system implementation including T123.7 member self-access patterns. Ready for T211 (Member Management) and T321 (Financial Management) endpoint integration.*