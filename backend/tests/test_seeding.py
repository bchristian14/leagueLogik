"""
Unit tests for database seeding utilities.

This module tests the admin user seeding functionality including password
hashing, user creation, idempotency, and credential validation.
"""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import AdminRole, MemberStatus, MemberType, User
from app.utils.seeding import (admin_exists, create_admin_user, get_admin_user,
                               hash_password, seed_admin_user,
                               validate_admin_credentials, verify_password)

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestPasswordHashing:
    """Test password hashing and verification functions."""

    def test_hash_password_creates_hash(self):
        """Test that password hashing creates a hash."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 50  # bcrypt hashes are typically 60+ characters
        assert hashed.startswith("$2b$")  # bcrypt identifier

    def test_hash_password_different_salts(self):
        """Test that identical passwords get different hashes (different salts)."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword456"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self):
        """Test password verification with empty password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False


class TestAdminUserQueries:
    """Test admin user query functions."""

    def test_admin_exists_false_empty_db(self, db_session):
        """Test admin_exists returns False when no users exist."""
        assert admin_exists(db_session) is False

    def test_admin_exists_false_no_admin(self, db_session):
        """Test admin_exists returns False when no admin users exist."""
        # Create a regular user (not admin)
        user = User(
            email="user@test.com",
            password_hash=hash_password("password"),
            first_name="Test",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            signup_date=date.today(),
        )
        db_session.add(user)
        db_session.commit()

        assert admin_exists(db_session) is False

    def test_admin_exists_true_with_admin(self, db_session):
        """Test admin_exists returns True when admin user exists."""
        # Create an admin user
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("password"),
            first_name="Admin",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            admin_roles=AdminRole.ADMIN,
            signup_date=date.today(),
        )
        db_session.add(admin)
        db_session.commit()

        assert admin_exists(db_session) is True

    def test_get_admin_user_none_empty_db(self, db_session):
        """Test get_admin_user returns None when no users exist."""
        assert get_admin_user(db_session) is None

    def test_get_admin_user_none_no_admin(self, db_session):
        """Test get_admin_user returns None when no admin users exist."""
        # Create a regular user (not admin)
        user = User(
            email="user@test.com",
            password_hash=hash_password("password"),
            first_name="Test",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            signup_date=date.today(),
        )
        db_session.add(user)
        db_session.commit()

        assert get_admin_user(db_session) is None

    def test_get_admin_user_returns_admin(self, db_session):
        """Test get_admin_user returns admin user when one exists."""
        # Create an admin user
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("password"),
            first_name="Admin",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            admin_roles=AdminRole.ADMIN,
            signup_date=date.today(),
        )
        db_session.add(admin)
        db_session.commit()

        retrieved_admin = get_admin_user(db_session)
        assert retrieved_admin is not None
        assert retrieved_admin.email == "admin@test.com"
        assert retrieved_admin.admin_roles == AdminRole.ADMIN


class TestCreateAdminUser:
    """Test admin user creation function."""

    def test_create_admin_user_success(self, db_session):
        """Test successful admin user creation."""
        admin = create_admin_user(
            db=db_session,
            email="admin@test.com",
            password="testpassword123",
            first_name="Test",
            last_name="Admin",
        )

        assert admin.email == "admin@test.com"
        assert admin.first_name == "Test"
        assert admin.last_name == "Admin"
        assert admin.admin_roles == AdminRole.ADMIN
        assert admin.member_status == MemberStatus.ACTIVE
        assert admin.member_type == MemberType.FULL
        assert verify_password("testpassword123", admin.password_hash)

    def test_create_admin_user_duplicate_raises_error(self, db_session):
        """Test that creating duplicate admin raises ValueError."""
        # Create first admin
        create_admin_user(
            db=db_session,
            email="admin1@test.com",
            password="password1",
            first_name="Admin",
            last_name="One",
        )

        # Try to create second admin without force
        with pytest.raises(ValueError, match="Admin user already exists"):
            create_admin_user(
                db=db_session,
                email="admin2@test.com",
                password="password2",
                first_name="Admin",
                last_name="Two",
            )

    def test_create_admin_user_force_update(self, db_session):
        """Test updating existing admin user with force=True."""
        # Create first admin
        admin1 = create_admin_user(
            db=db_session,
            email="admin@test.com",
            password="password1",
            first_name="Admin",
            last_name="One",
        )

        # Update with force=True
        admin2 = create_admin_user(
            db=db_session,
            email="updated@test.com",
            password="password2",
            first_name="Admin",
            last_name="Two",
            force=True,
        )

        # Should be the same database record (same ID)
        assert admin1.member_id == admin2.member_id
        assert admin2.email == "updated@test.com"
        assert admin2.first_name == "Admin"
        assert admin2.last_name == "Two"
        assert verify_password("password2", admin2.password_hash)

    def test_create_admin_user_uses_defaults(self, db_session):
        """Test that create_admin_user uses settings defaults when args are None."""
        with patch("app.utils.seeding.settings") as mock_settings:
            mock_settings.admin_email = "default@test.com"
            mock_settings.admin_password = "defaultpass"
            mock_settings.admin_first_name = "Default"
            mock_settings.admin_last_name = "Admin"

            admin = create_admin_user(db=db_session)

            assert admin.email == "default@test.com"
            assert admin.first_name == "Default"
            assert admin.last_name == "Admin"
            assert verify_password("defaultpass", admin.password_hash)


class TestSeedAdminUser:
    """Test the main seeding function."""

    @patch("app.utils.seeding.SessionLocal")
    def test_seed_admin_user_success(self, mock_session_local, db_session):
        """Test successful admin user seeding."""
        # Mock SessionLocal to return our test session
        mock_session_local.return_value = db_session

        admin = seed_admin_user(
            email="admin@test.com",
            password="testpassword",
            first_name="Test",
            last_name="Admin",
        )

        assert admin is not None
        assert admin.email == "admin@test.com"
        assert admin.admin_roles == AdminRole.ADMIN

    @patch("app.utils.seeding.SessionLocal")
    def test_seed_admin_user_dry_run(self, mock_session_local, db_session):
        """Test dry run mode returns None without creating user."""
        mock_session_local.return_value = db_session

        result = seed_admin_user(
            email="admin@test.com", password="testpassword", dry_run=True
        )

        assert result is None
        assert not admin_exists(db_session)

    @patch("app.utils.seeding.SessionLocal")
    def test_seed_admin_user_force_existing(self, mock_session_local, db_session):
        """Test force update of existing admin user."""
        mock_session_local.return_value = db_session

        # Create initial admin
        admin1 = seed_admin_user(
            email="admin@test.com",
            password="password1",
            first_name="Admin",
            last_name="One",
        )

        # Update with force
        admin2 = seed_admin_user(
            email="updated@test.com",
            password="password2",
            first_name="Admin",
            last_name="Two",
            force=True,
        )

        assert admin1.member_id == admin2.member_id
        assert admin2.email == "updated@test.com"


class TestValidateAdminCredentials:
    """Test admin credential validation function."""

    @patch("app.utils.seeding.SessionLocal")
    def test_validate_admin_credentials_success(self, mock_session_local, db_session):
        """Test successful credential validation."""
        mock_session_local.return_value = db_session

        # Create admin user
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("testpassword"),
            first_name="Admin",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            admin_roles=AdminRole.ADMIN,
            signup_date=date.today(),
        )
        db_session.add(admin)
        db_session.commit()

        # Validate credentials
        is_valid = validate_admin_credentials("admin@test.com", "testpassword")
        assert is_valid is True

    @patch("app.utils.seeding.SessionLocal")
    def test_validate_admin_credentials_wrong_password(
        self, mock_session_local, db_session
    ):
        """Test credential validation with wrong password."""
        mock_session_local.return_value = db_session

        # Create admin user
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("testpassword"),
            first_name="Admin",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            admin_roles=AdminRole.ADMIN,
            signup_date=date.today(),
        )
        db_session.add(admin)
        db_session.commit()

        # Validate with wrong password
        is_valid = validate_admin_credentials("admin@test.com", "wrongpassword")
        assert is_valid is False

    @patch("app.utils.seeding.SessionLocal")
    def test_validate_admin_credentials_user_not_found(
        self, mock_session_local, db_session
    ):
        """Test credential validation when admin user doesn't exist."""
        mock_session_local.return_value = db_session

        # Validate non-existent user
        is_valid = validate_admin_credentials("notfound@test.com", "password")
        assert is_valid is False

    @patch("app.utils.seeding.SessionLocal")
    def test_validate_admin_credentials_not_admin(self, mock_session_local, db_session):
        """Test credential validation for user without admin role."""
        mock_session_local.return_value = db_session

        # Create regular user (not admin)
        user = User(
            email="user@test.com",
            password_hash=hash_password("testpassword"),
            first_name="Regular",
            last_name="User",
            member_status=MemberStatus.ACTIVE,
            member_type=MemberType.FULL,
            signup_date=date.today(),
            # No admin_roles set
        )
        db_session.add(user)
        db_session.commit()

        # Try to validate as admin
        is_valid = validate_admin_credentials("user@test.com", "testpassword")
        assert is_valid is False
