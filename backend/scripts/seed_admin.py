#!/usr/bin/env python3
"""
Admin user seeding script for Golf League Management System.

This script creates an initial admin user for the system. It can be run
from the command line and provides various options for admin user creation.

Usage:
    python scripts/seed_admin.py                    # Standard seeding
    python scripts/seed_admin.py --dry-run          # Preview without changes
    python scripts/seed_admin.py --verbose          # Detailed output
    python scripts/seed_admin.py --force            # Override existing admin
    python scripts/seed_admin.py --help             # Show help

Environment Variables:
    ADMIN_EMAIL: Admin user email (default: admin@leaguelogik.com)
    ADMIN_PASSWORD: Admin user password (default: admin123!)
    ADMIN_FIRST_NAME: Admin first name (default: League)
    ADMIN_LAST_NAME: Admin last name (default: Administrator)
"""

import argparse
import logging
import sys
from pathlib import Path

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.settings import settings
from app.utils.seeding import seed_admin_user, validate_admin_credentials


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration for the script.

    Args:
        verbose: If True, enables debug level logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """Main script execution function."""
    parser = argparse.ArgumentParser(
        description="Seed admin user for Golf League Management System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the operation without making changes",
    )

    parser.add_argument(
        "--force", action="store_true", help="Update existing admin user if one exists"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging output"
    )

    parser.add_argument(
        "--email",
        type=str,
        help=f"Admin email address (default: {settings.admin_email})",
    )

    parser.add_argument(
        "--password",
        type=str,
        help="Admin password (default: from settings/environment)",
    )

    parser.add_argument(
        "--first-name",
        type=str,
        help=f"Admin first name (default: {settings.admin_first_name})",
    )

    parser.add_argument(
        "--last-name",
        type=str,
        help=f"Admin last name (default: {settings.admin_last_name})",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate admin credentials after creation/update",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting admin user seeding script")
        logger.info(f"Dry run: {args.dry_run}")
        logger.info(f"Force update: {args.force}")

        if args.dry_run:
            logger.info("DRY RUN MODE: No changes will be made to the database")

        # Perform seeding operation
        admin_user = seed_admin_user(
            email=args.email,
            password=args.password,
            first_name=args.first_name,
            last_name=args.last_name,
            force=args.force,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            logger.info("Dry run completed successfully")
            print("\\nDRY RUN SUMMARY:")
            print(f"Target admin email: {args.email or settings.admin_email}")
            print(
                f"Admin name: {args.first_name or settings.admin_first_name} {args.last_name or settings.admin_last_name}"
            )
            print(f"Force update: {args.force}")
            print("\\nNo changes were made to the database.")
            return

        if admin_user:
            logger.info("Admin user seeding completed successfully")
            print("\\nSUCCESS:")
            print(f"Admin user: {admin_user.email}")
            print(f"Name: {admin_user.full_name}")
            print(f"Member ID: {admin_user.member_id}")
            print(f"Admin Role: {admin_user.admin_roles}")
            print(f"Status: {admin_user.member_status}")

            # Validate credentials if requested
            if args.validate:
                logger.info("Validating admin credentials...")
                password = args.password or settings.admin_password

                if validate_admin_credentials(admin_user.email, password):
                    print("\\nCREDENTIAL VALIDATION: ✅ PASSED")
                    logger.info("Admin credentials validated successfully")
                else:
                    print("\\nCREDENTIAL VALIDATION: ❌ FAILED")
                    logger.error("Admin credential validation failed")
                    sys.exit(1)

        else:
            logger.warning("No admin user was created (may already exist)")
            print("\\nWARNING: No admin user was created.")
            print("This may indicate an admin user already exists.")
            print("Use --force to update existing admin or --dry-run to preview.")

    except ValueError as e:
        logger.error(f"Seeding failed: {e}")
        print(f"\\nERROR: {e}")
        print("\\nTo update an existing admin user, use the --force flag.")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error during seeding: {e}")
        print(f"\\nUNEXPECTED ERROR: {e}")
        print("\\nCheck the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
