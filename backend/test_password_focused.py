#!/usr/bin/env python3
"""
Focused test script for specific password security features with correct admin credentials.
"""

import json
import time
import requests
from datetime import datetime, timezone


def test_password_change():
    """Test password change functionality with correct admin credentials."""
    base_url = "http://localhost:8000/api/v1"
    admin_email = "admin@leaguelogik.com"
    admin_password = "Admin123!"  # Updated password meeting requirements

    print("=" * 60)
    print("FOCUSED PASSWORD SECURITY TESTS")
    print("=" * 60)

    # 1. Login with correct credentials
    print("1. Testing login with updated admin credentials...")
    login_response = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": admin_email,
            "password": admin_password
        }
    )

    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.json() if login_response.content else 'No content'}")
        return False

    print("✅ Login successful!")
    access_token = login_response.json()["access_token"]

    # 2. Test password change with valid current password
    print("\n2. Testing password change with valid current password...")
    new_password = "NewSecure123!"

    change_response = requests.post(
        f"{base_url}/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": admin_password,
            "new_password": new_password,
            "confirm_password": new_password
        }
    )

    if change_response.status_code != 200:
        print(f"❌ Password change failed: {change_response.status_code}")
        print(f"Response: {change_response.json() if change_response.content else 'No content'}")
        return False

    print("✅ Password change successful!")
    print(f"Response: {change_response.json()}")

    # 3. Verify login with new password
    print("\n3. Testing login with new password...")
    new_login_response = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": admin_email,
            "password": new_password
        }
    )

    if new_login_response.status_code != 200:
        print(f"❌ Login with new password failed: {new_login_response.status_code}")
        return False

    print("✅ Login with new password successful!")
    new_token = new_login_response.json()["access_token"]

    # 4. Restore original password
    print("\n4. Restoring original password...")
    restore_response = requests.post(
        f"{base_url}/auth/change-password",
        headers={"Authorization": f"Bearer {new_token}"},
        json={
            "current_password": new_password,
            "new_password": admin_password,
            "confirm_password": admin_password
        }
    )

    if restore_response.status_code != 200:
        print(f"❌ Password restore failed: {restore_response.status_code}")
        print(f"Response: {restore_response.json() if restore_response.content else 'No content'}")
        return False

    print("✅ Password restored successfully!")

    return True


def test_invalid_current_password():
    """Test password change with invalid current password."""
    base_url = "http://localhost:8000/api/v1"
    admin_email = "admin@leaguelogik.com"
    admin_password = "Admin123!"

    print("\n5. Testing password change with invalid current password...")

    # Login first
    login_response = requests.post(
        f"{base_url}/auth/login",
        json={"email": admin_email, "password": admin_password}
    )

    if login_response.status_code != 200:
        print("❌ Could not login for invalid password test")
        return False

    access_token = login_response.json()["access_token"]

    # Try to change password with wrong current password
    response = requests.post(
        f"{base_url}/auth/change-password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
            "confirm_password": "NewPassword123!"
        }
    )

    if response.status_code == 400:
        error_detail = response.json().get("detail", "").lower()
        if "current password is incorrect" in error_detail:
            print("✅ Correctly rejected invalid current password")
            print(f"Error message: {response.json()['detail']}")
            return True
        else:
            print(f"❌ Wrong error message: {response.json()}")
            return False
    else:
        print(f"❌ Expected 400 status, got {response.status_code}")
        print(f"Response: {response.json() if response.content else 'No content'}")
        return False


def test_account_lockout():
    """Test account lockout mechanism."""
    base_url = "http://localhost:8000/api/v1"
    admin_email = "admin@leaguelogik.com"
    admin_password = "Admin123!"

    print("\n6. Testing account lockout mechanism...")

    # First verify account works
    test_response = requests.post(
        f"{base_url}/auth/login",
        json={"email": admin_email, "password": admin_password}
    )

    if test_response.status_code != 200:
        print("❌ Account may already be locked or credentials invalid")
        return False

    print("✅ Baseline: Account works with correct credentials")

    # Make 5 failed attempts
    print("Making 5 failed login attempts...")
    for i in range(1, 6):
        response = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": admin_email,
                "password": "WrongPassword123!"
            }
        )

        if response.status_code == 401:
            print(f"  Failed attempt {i}/5: ✅ Status 401")
        else:
            print(f"  Failed attempt {i}/5: ❌ Status {response.status_code}")
            return False

    # Now try with correct password - should be locked
    print("Testing login with correct password after 5 failed attempts...")
    locked_response = requests.post(
        f"{base_url}/auth/login",
        json={
            "email": admin_email,
            "password": admin_password
        }
    )

    if locked_response.status_code == 401:
        print("✅ Account correctly locked - correct password rejected")

        # Test that it stays locked for a bit
        time.sleep(2)
        still_locked_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": admin_email,
                "password": admin_password
            }
        )

        if still_locked_response.status_code == 401:
            print("✅ Account remains locked after short wait")
            print("Note: Full 15-minute lockout not tested due to time constraints")
            return True
        else:
            print("❌ Account unlocked too quickly")
            return False
    else:
        print(f"❌ Account not locked! Status: {locked_response.status_code}")
        return False


if __name__ == "__main__":
    print(f"Starting focused tests at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")

    tests = [
        ("Password Change Functionality", test_password_change),
        ("Invalid Current Password", test_invalid_current_password),
        ("Account Lockout", test_account_lockout),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")

            # Delay between tests
            time.sleep(1)

        except Exception as e:
            print(f"❌ {test_name} EXCEPTION: {str(e)}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total} ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("🎉 All focused tests passed!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")

    print(f"Completed at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")