"""
Test suite for the core role system implementation.

This module provides comprehensive tests for role-based access control,
including role inheritance, permission checking, and dependency factories.
"""

import pytest
from unittest.mock import Mock
from fastapi import HTTPException, status

from app.models.user import User, AdminRole, MemberStatus, MemberType
from app.api.dependencies import get_user_roles, require_roles


class TestGetUserRoles:
    """Test cases for the get_user_roles function."""

    def test_regular_member_no_roles(self):
        """Test that regular members with no admin roles return empty set."""
        user = Mock(spec=User)
        user.admin_roles = None

        result = get_user_roles(user)

        assert result == set()

    def test_admin_inherits_all_roles(self):
        """Test that ADMIN role inherits all other admin roles."""
        user = Mock(spec=User)
        user.admin_roles = AdminRole.ADMIN

        result = get_user_roles(user)

        # Admin should have all roles
        expected = {
            AdminRole.ADMIN,
            AdminRole.TREASURER,
            AdminRole.COURSE_COORDINATOR,
            AdminRole.TOURNAMENT_COORDINATOR
        }
        assert result == expected
        assert result == set(AdminRole)

    def test_treasurer_specific_role(self):
        """Test that TREASURER role only has treasurer permissions."""
        user = Mock(spec=User)
        user.admin_roles = AdminRole.TREASURER

        result = get_user_roles(user)

        assert result == {AdminRole.TREASURER}

    def test_course_coordinator_specific_role(self):
        """Test that COURSE_COORDINATOR role only has course coordinator permissions."""
        user = Mock(spec=User)
        user.admin_roles = AdminRole.COURSE_COORDINATOR

        result = get_user_roles(user)

        assert result == {AdminRole.COURSE_COORDINATOR}

    def test_tournament_coordinator_specific_role(self):
        """Test that TOURNAMENT_COORDINATOR role only has tournament coordinator permissions."""
        user = Mock(spec=User)
        user.admin_roles = AdminRole.TOURNAMENT_COORDINATOR

        result = get_user_roles(user)

        assert result == {AdminRole.TOURNAMENT_COORDINATOR}


class TestRequireRoles:
    """Test cases for the require_roles dependency factory."""

    def test_single_role_requirement_success(self):
        """Test successful access with single role requirement."""
        # Create mock user with treasurer role
        user = Mock(spec=User)
        user.admin_roles = AdminRole.TREASURER

        # Create dependency function
        dependency = require_roles(AdminRole.TREASURER)

        # Mock get_current_user to return our user
        result = dependency(current_user=user)

        assert result == user

    def test_single_role_requirement_admin_inheritance(self):
        """Test that admin can access endpoints requiring specific roles."""
        # Create mock user with admin role
        user = Mock(spec=User)
        user.admin_roles = AdminRole.ADMIN

        # Create dependency function requiring treasurer
        dependency = require_roles(AdminRole.TREASURER)

        result = dependency(current_user=user)

        assert result == user

    def test_multiple_role_requirement_success(self):
        """Test successful access with multiple role options."""
        # Create mock user with course coordinator role
        user = Mock(spec=User)
        user.admin_roles = AdminRole.COURSE_COORDINATOR

        # Create dependency function allowing either treasurer or course coordinator
        dependency = require_roles(AdminRole.TREASURER, AdminRole.COURSE_COORDINATOR)

        result = dependency(current_user=user)

        assert result == user

    def test_role_requirement_failure_regular_member(self):
        """Test access denied for regular member without admin roles."""
        # Create mock user with no admin roles
        user = Mock(spec=User)
        user.admin_roles = None

        # Create dependency function requiring admin
        dependency = require_roles(AdminRole.ADMIN)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in exc_info.value.detail
        assert "Admin" in exc_info.value.detail

    def test_role_requirement_failure_insufficient_role(self):
        """Test access denied when user has different admin role."""
        # Create mock user with tournament coordinator role
        user = Mock(spec=User)
        user.admin_roles = AdminRole.TOURNAMENT_COORDINATOR

        # Create dependency function requiring treasurer
        dependency = require_roles(AdminRole.TREASURER)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in exc_info.value.detail
        assert "Treasurer" in exc_info.value.detail

    def test_single_role_error_message(self):
        """Test error message format for single role requirement."""
        user = Mock(spec=User)
        user.admin_roles = None

        dependency = require_roles(AdminRole.COURSE_COORDINATOR)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        assert exc_info.value.detail == "Access denied. This endpoint requires Course Coordinator role."

    def test_multiple_role_error_message(self):
        """Test error message format for multiple role requirement."""
        user = Mock(spec=User)
        user.admin_roles = None

        dependency = require_roles(AdminRole.TREASURER, AdminRole.ADMIN)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        expected_detail = "Access denied. This endpoint requires one of the following roles: Treasurer, Admin."
        assert exc_info.value.detail == expected_detail

    def test_role_name_formatting_underscore_replacement(self):
        """Test that role names with underscores are formatted properly in error messages."""
        user = Mock(spec=User)
        user.admin_roles = None

        dependency = require_roles(AdminRole.TOURNAMENT_COORDINATOR)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        assert "Tournament Coordinator" in exc_info.value.detail

    def test_all_roles_requirement(self):
        """Test dependency requiring any admin role."""
        # Test admin can access
        admin_user = Mock(spec=User)
        admin_user.admin_roles = AdminRole.ADMIN

        dependency = require_roles(*AdminRole)
        result = dependency(current_user=admin_user)
        assert result == admin_user

        # Test specific role can access
        treasurer_user = Mock(spec=User)
        treasurer_user.admin_roles = AdminRole.TREASURER

        result = dependency(current_user=treasurer_user)
        assert result == treasurer_user

        # Test regular member cannot access
        regular_user = Mock(spec=User)
        regular_user.admin_roles = None

        with pytest.raises(HTTPException):
            dependency(current_user=regular_user)


class TestRoleInheritanceLogic:
    """Test cases specifically for role inheritance patterns."""

    def test_admin_can_access_all_role_specific_endpoints(self):
        """Test that admin user can access endpoints for any specific role."""
        admin_user = Mock(spec=User)
        admin_user.admin_roles = AdminRole.ADMIN

        # Test admin can access treasurer endpoints
        treasurer_dep = require_roles(AdminRole.TREASURER)
        result = treasurer_dep(current_user=admin_user)
        assert result == admin_user

        # Test admin can access course coordinator endpoints
        course_dep = require_roles(AdminRole.COURSE_COORDINATOR)
        result = course_dep(current_user=admin_user)
        assert result == admin_user

        # Test admin can access tournament coordinator endpoints
        tournament_dep = require_roles(AdminRole.TOURNAMENT_COORDINATOR)
        result = tournament_dep(current_user=admin_user)
        assert result == admin_user

    def test_specific_roles_cannot_access_other_specific_roles(self):
        """Test that specific roles cannot access endpoints for other specific roles."""
        treasurer_user = Mock(spec=User)
        treasurer_user.admin_roles = AdminRole.TREASURER

        # Treasurer cannot access course coordinator endpoints
        course_dep = require_roles(AdminRole.COURSE_COORDINATOR)
        with pytest.raises(HTTPException):
            course_dep(current_user=treasurer_user)

        # Treasurer cannot access tournament coordinator endpoints
        tournament_dep = require_roles(AdminRole.TOURNAMENT_COORDINATOR)
        with pytest.raises(HTTPException):
            tournament_dep(current_user=treasurer_user)

    def test_role_combination_access_patterns(self):
        """Test access patterns with multiple role combinations."""
        # Admin should be able to access financial endpoints (treasurer + admin)
        admin_user = Mock(spec=User)
        admin_user.admin_roles = AdminRole.ADMIN

        financial_dep = require_roles(AdminRole.TREASURER, AdminRole.ADMIN)
        result = financial_dep(current_user=admin_user)
        assert result == admin_user

        # Treasurer should be able to access financial endpoints
        treasurer_user = Mock(spec=User)
        treasurer_user.admin_roles = AdminRole.TREASURER

        result = financial_dep(current_user=treasurer_user)
        assert result == treasurer_user

        # Course coordinator should NOT be able to access financial endpoints
        course_user = Mock(spec=User)
        course_user.admin_roles = AdminRole.COURSE_COORDINATOR

        with pytest.raises(HTTPException):
            financial_dep(current_user=course_user)


class TestConvenienceDependencies:
    """Test cases for convenience dependency functions."""

    def test_require_admin_convenience(self):
        """Test require_admin convenience function."""
        from app.api.dependencies import require_admin

        # Admin should pass
        admin_user = Mock(spec=User)
        admin_user.admin_roles = AdminRole.ADMIN

        dependency = require_admin()
        result = dependency(current_user=admin_user)
        assert result == admin_user

        # Other roles should fail
        treasurer_user = Mock(spec=User)
        treasurer_user.admin_roles = AdminRole.TREASURER

        with pytest.raises(HTTPException):
            dependency(current_user=treasurer_user)

    def test_require_financial_access_convenience(self):
        """Test require_financial_access convenience function."""
        from app.api.dependencies import require_financial_access

        dependency = require_financial_access()

        # Admin should pass
        admin_user = Mock(spec=User)
        admin_user.admin_roles = AdminRole.ADMIN

        result = dependency(current_user=admin_user)
        assert result == admin_user

        # Treasurer should pass
        treasurer_user = Mock(spec=User)
        treasurer_user.admin_roles = AdminRole.TREASURER

        result = dependency(current_user=treasurer_user)
        assert result == treasurer_user

        # Other roles should fail
        course_user = Mock(spec=User)
        course_user.admin_roles = AdminRole.COURSE_COORDINATOR

        with pytest.raises(HTTPException):
            dependency(current_user=course_user)

    def test_require_any_admin_convenience(self):
        """Test require_any_admin convenience function."""
        from app.api.dependencies import require_any_admin

        dependency = require_any_admin()

        # All admin roles should pass
        for role in AdminRole:
            user = Mock(spec=User)
            user.admin_roles = role

            result = dependency(current_user=user)
            assert result == user

        # Regular member should fail
        regular_user = Mock(spec=User)
        regular_user.admin_roles = None

        with pytest.raises(HTTPException):
            dependency(current_user=regular_user)


class TestEdgeCases:
    """Test cases for edge cases and error conditions."""

    def test_empty_roles_requirement(self):
        """Test behavior when no roles are specified (should allow anyone)."""
        user = Mock(spec=User)
        user.admin_roles = None

        # This should not fail even for regular users since no roles are required
        dependency = require_roles()
        result = dependency(current_user=user)
        assert result == user

    def test_none_user_admin_roles_property(self):
        """Test get_user_roles with user having None admin_roles."""
        user = Mock(spec=User)
        user.admin_roles = None

        result = get_user_roles(user)
        assert result == set()
        assert isinstance(result, set)

    def test_role_intersection_logic(self):
        """Test the intersection logic used in require_roles."""
        # Test that intersection works correctly
        user_roles = {AdminRole.ADMIN, AdminRole.TREASURER, AdminRole.COURSE_COORDINATOR, AdminRole.TOURNAMENT_COORDINATOR}
        required_roles = {AdminRole.TREASURER}

        # Should have intersection
        assert user_roles.intersection(required_roles)

        # Test no intersection
        user_roles = {AdminRole.COURSE_COORDINATOR}
        required_roles = {AdminRole.TREASURER, AdminRole.ADMIN}

        # Should have no intersection
        assert not user_roles.intersection(required_roles)

    def test_set_adminrole_conversion(self):
        """Test that set(AdminRole) returns all enum values."""
        all_roles = set(AdminRole)
        expected = {
            AdminRole.ADMIN,
            AdminRole.TREASURER,
            AdminRole.COURSE_COORDINATOR,
            AdminRole.TOURNAMENT_COORDINATOR
        }
        assert all_roles == expected


class TestRequireMemberSelfOrAdmin:
    """Test cases for the require_member_self_or_admin dependency factory."""

    def test_member_self_access_success(self):
        """Test that member can access their own data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()

        # Create mock user accessing their own data
        user = Mock(spec=User)
        user.member_id = member_id
        user.admin_roles = None

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should succeed since user is accessing their own data
        result = dependency(current_user=user)
        assert result == user

    def test_admin_access_any_member_success(self):
        """Test that admin can access any member's data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        admin_member_id = uuid.uuid4()  # Different member ID

        # Create mock admin user accessing another member's data
        admin_user = Mock(spec=User)
        admin_user.member_id = admin_member_id
        admin_user.admin_roles = AdminRole.ADMIN

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should succeed since user is admin
        result = dependency(current_user=admin_user)
        assert result == admin_user

    def test_treasurer_access_any_member_success(self):
        """Test that treasurer can access any member's data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        treasurer_member_id = uuid.uuid4()  # Different member ID

        # Create mock treasurer user accessing another member's data
        treasurer_user = Mock(spec=User)
        treasurer_user.member_id = treasurer_member_id
        treasurer_user.admin_roles = AdminRole.TREASURER

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should succeed since user has admin role
        result = dependency(current_user=treasurer_user)
        assert result == treasurer_user

    def test_course_coordinator_access_any_member_success(self):
        """Test that course coordinator can access any member's data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        coordinator_member_id = uuid.uuid4()  # Different member ID

        # Create mock course coordinator accessing another member's data
        coordinator_user = Mock(spec=User)
        coordinator_user.member_id = coordinator_member_id
        coordinator_user.admin_roles = AdminRole.COURSE_COORDINATOR

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should succeed since user has admin role
        result = dependency(current_user=coordinator_user)
        assert result == coordinator_user

    def test_tournament_coordinator_access_any_member_success(self):
        """Test that tournament coordinator can access any member's data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        coordinator_member_id = uuid.uuid4()  # Different member ID

        # Create mock tournament coordinator accessing another member's data
        coordinator_user = Mock(spec=User)
        coordinator_user.member_id = coordinator_member_id
        coordinator_user.admin_roles = AdminRole.TOURNAMENT_COORDINATOR

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should succeed since user has admin role
        result = dependency(current_user=coordinator_user)
        assert result == coordinator_user

    def test_member_cross_access_denied(self):
        """Test that regular member cannot access other member's data."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        other_member_id = uuid.uuid4()  # Different member ID

        # Create mock regular member trying to access another member's data
        user = Mock(spec=User)
        user.member_id = other_member_id
        user.admin_roles = None

        # Create dependency function
        dependency = require_member_self_or_admin(member_id)

        # Should fail since user is not accessing their own data and has no admin roles
        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in exc_info.value.detail
        assert "your own data" in exc_info.value.detail
        assert "administrative privileges" in exc_info.value.detail

    def test_error_message_format(self):
        """Test the specific error message format for access denied."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        other_member_id = uuid.uuid4()

        user = Mock(spec=User)
        user.member_id = other_member_id
        user.admin_roles = None

        dependency = require_member_self_or_admin(member_id)

        with pytest.raises(HTTPException) as exc_info:
            dependency(current_user=user)

        expected_detail = "Access denied. You can only access your own data unless you have administrative privileges."
        assert exc_info.value.detail == expected_detail

    def test_admin_role_inheritance_for_member_access(self):
        """Test that admin role inheritance works for member data access."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()
        admin_member_id = uuid.uuid4()

        # Admin should be able to access any member's data due to role inheritance
        admin_user = Mock(spec=User)
        admin_user.member_id = admin_member_id
        admin_user.admin_roles = AdminRole.ADMIN

        dependency = require_member_self_or_admin(member_id)
        result = dependency(current_user=admin_user)
        assert result == admin_user

    def test_same_member_id_comparison(self):
        """Test exact UUID comparison for self-access."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        # Use the exact same UUID instance
        member_id = uuid.uuid4()

        user = Mock(spec=User)
        user.member_id = member_id  # Same UUID
        user.admin_roles = None

        dependency = require_member_self_or_admin(member_id)
        result = dependency(current_user=user)
        assert result == user

    def test_different_uuid_instances_same_value(self):
        """Test that UUID comparison works with different instances of same value."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        # Create UUID from string to ensure different instances with same value
        uuid_str = str(uuid.uuid4())
        member_id = uuid.UUID(uuid_str)
        user_member_id = uuid.UUID(uuid_str)

        user = Mock(spec=User)
        user.member_id = user_member_id  # Different instance, same value
        user.admin_roles = None

        dependency = require_member_self_or_admin(member_id)
        result = dependency(current_user=user)
        assert result == user

    def test_edge_case_none_admin_roles(self):
        """Test behavior with None admin_roles (regular member)."""
        import uuid
        from app.api.dependencies import require_member_self_or_admin

        member_id = uuid.uuid4()

        # Regular member with None admin_roles accessing own data
        user = Mock(spec=User)
        user.member_id = member_id
        user.admin_roles = None

        dependency = require_member_self_or_admin(member_id)
        result = dependency(current_user=user)
        assert result == user