#!/usr/bin/env python3
"""
Comprehensive test for password validation rules.
"""

import requests
import json
from datetime import datetime, timezone


def test_password_validation():
    """Test all password validation rules comprehensively."""
    base_url = "http://localhost:8000/api/v1"
    admin_email = "admin@leaguelogik.com"
    admin_password = "Admin123!"

    print("=" * 60)
    print("PASSWORD VALIDATION RULES TEST")
    print("=" * 60)

    # First, unlock the account by resetting failed attempts
    print("Resetting account lockout...")
    reset_response = requests.post(f"{base_url}/auth/login", json={"email": admin_email, "password": admin_password})

    if reset_response.status_code != 200:
        print("❌ Need to reset account lockout manually")
        return False

    access_token = reset_response.json()["access_token"]
    print("✅ Account unlocked and ready for testing")

    # Test cases for password validation
    validation_tests = [
        {
            "name": "Password too short (7 chars)",
            "password": "Short1!",
            "confirm": "Short1!",
            "expected_error": "at least 8 characters",
            "should_fail": True
        },
        {
            "name": "Password exactly 8 chars (boundary)",
            "password": "Valid1!A",
            "confirm": "Valid1!A",
            "should_fail": False
        },
        {
            "name": "No uppercase letter",
            "password": "nouppercase123!",
            "confirm": "nouppercase123!",
            "expected_error": "uppercase letter",
            "should_fail": True
        },
        {
            "name": "No lowercase letter",
            "password": "NOLOWERCASE123!",
            "confirm": "NOLOWERCASE123!",
            "expected_error": "lowercase letter",
            "should_fail": True
        },
        {
            "name": "No digit",
            "password": "NoDigitsHere!",
            "confirm": "NoDigitsHere!",
            "expected_error": "digit",
            "should_fail": True
        },
        {
            "name": "No special character",
            "password": "NoSpecialChar123",
            "confirm": "NoSpecialChar123",
            "expected_error": "special character",
            "should_fail": True
        },
        {
            "name": "Password mismatch",
            "password": "ValidPassword123!",
            "confirm": "DifferentPassword123!",
            "expected_error": "do not match",
            "should_fail": True
        },
        {
            "name": "All requirements met",
            "password": "ValidPassword123!",
            "confirm": "ValidPassword123!",
            "should_fail": False
        },
        {
            "name": "Complex valid password",
            "password": "MyC0mpl3x!P@ssw0rd",
            "confirm": "MyC0mpl3x!P@ssw0rd",
            "should_fail": False
        },
        {
            "name": "Maximum length boundary (100 chars)",
            "password": "A1!" + "x" * 97,  # 100 chars total
            "confirm": "A1!" + "x" * 97,
            "should_fail": False
        },
        {
            "name": "Over maximum length (101 chars)",
            "password": "A1!" + "x" * 98,  # 101 chars total
            "confirm": "A1!" + "x" * 98,
            "expected_error": "100 characters",
            "should_fail": True
        }
    ]

    passed = 0
    total = len(validation_tests)

    for i, test in enumerate(validation_tests, 1):
        print(f"\n{i}. Testing: {test['name']}")
        print(f"   Password: {test['password'][:30]}{'...' if len(test['password']) > 30 else ''}")

        response = requests.post(
            f"{base_url}/auth/change-password",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "current_password": admin_password,
                "new_password": test["password"],
                "confirm_password": test["confirm"]
            }
        )

        if test["should_fail"]:
            if response.status_code == 422:
                error_data = response.json()
                error_text = str(error_data).lower()

                if "expected_error" in test and test["expected_error"].lower() in error_text:
                    print(f"   ✅ PASS - Correctly rejected with expected error")
                    print(f"   Expected: {test['expected_error']}")
                    passed += 1
                else:
                    print(f"   ❌ FAIL - Rejected but wrong error message")
                    print(f"   Expected: {test.get('expected_error', 'Any validation error')}")
                    print(f"   Got: {error_data}")
            else:
                print(f"   ❌ FAIL - Expected 422 status, got {response.status_code}")
                if response.content:
                    print(f"   Response: {response.json()}")
        else:
            if response.status_code == 200:
                print(f"   ✅ PASS - Correctly accepted valid password")
                passed += 1

                # Change password back to original for next test
                restore_response = requests.post(
                    f"{base_url}/auth/login",
                    json={"email": admin_email, "password": test["password"]}
                )

                if restore_response.status_code == 200:
                    new_token = restore_response.json()["access_token"]
                    requests.post(
                        f"{base_url}/auth/change-password",
                        headers={"Authorization": f"Bearer {new_token}"},
                        json={
                            "current_password": test["password"],
                            "new_password": admin_password,
                            "confirm_password": admin_password
                        }
                    )
                    print(f"   Password restored for next test")
            else:
                print(f"   ❌ FAIL - Expected 200 status, got {response.status_code}")
                if response.content:
                    print(f"   Response: {response.json()}")

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION RULES SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total} ({(passed/total)*100:.1f}%)")

    if passed == total:
        print("🎉 All validation rule tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} validation test(s) failed")
        return False


if __name__ == "__main__":
    print(f"Starting validation tests at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
    success = test_password_validation()
    print(f"Completed at {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
    exit(0 if success else 1)