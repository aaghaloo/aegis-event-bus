#!/usr/bin/env python3
"""
Database restore script for disaster recovery.
Restores PostgreSQL database from backup files.
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_database_url():
    """Get database URL from environment or config."""
    from app.config import settings

    return settings.DATABASE_URL


def list_backups(backup_dir: Path):
    """List available backup files."""
    backups = []
    for backup_file in backup_dir.glob("aegis_backup_*"):
        backups.append(
            {
                "filename": backup_file.name,
                "size": backup_file.stat().st_size,
                "modified": backup_file.stat().st_mtime,
            }
        )
    return sorted(backups, key=lambda x: x["modified"], reverse=True)


def restore_postgresql(database_url: str, backup_path: Path):
    """Restore PostgreSQL database using pg_restore."""
    try:
        # Parse database URL
        if database_url.startswith("postgresql://"):
            # Extract connection details
            url_parts = database_url.replace("postgresql://", "").split("/")
            if len(url_parts) != 2:
                raise ValueError("Invalid database URL format")

            connection_part = url_parts[0]
            database_name = url_parts[1]

            # Parse connection details
            if "@" in connection_part:
                auth_part, host_part = connection_part.split("@")
                username, password = auth_part.split(":")
                host, port = host_part.split(":")
            else:
                raise ValueError("Invalid database URL format")

            # Set environment variables for pg_restore
            env = os.environ.copy()
            env["PGPASSWORD"] = password

            # Build pg_restore command
            cmd = [
                "pg_restore",
                "-h",
                host,
                "-p",
                port,
                "-U",
                username,
                "-d",
                database_name,
                "--verbose",
                "--clean",
                "--no-password",
                str(backup_path),
            ]

            logger.info(f"Starting database restore from {backup_path}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info("Database restore completed successfully")
                return True
            else:
                logger.error(f"Restore failed: {result.stderr}")
                return False

        else:
            logger.error("Only PostgreSQL restores are supported")
            return False

    except Exception as e:
        logger.error(f"Restore failed: {str(e)}")
        return False


def restore_sqlite(database_url: str, backup_path: Path):
    """Restore SQLite database by copying the backup file."""
    try:
        # Extract database path from URL
        if database_url.startswith("sqlite:///"):
            db_path = database_url.replace("sqlite:///", "")
        elif database_url == "sqlite://":
            db_path = "eventbus.db"
        else:
            logger.error("Invalid SQLite URL format")
            return False

        # Create backup of current database if it exists
        if os.path.exists(db_path):
            import shutil
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            current_backup = f"{db_path}.backup_{timestamp}"
            shutil.copy2(db_path, current_backup)
            logger.info(f"Created backup of current database: {current_backup}")

        # Copy backup to database location
        import shutil

        shutil.copy2(backup_path, db_path)

        logger.info(f"SQLite restore completed from {backup_path}")
        return True

    except Exception as e:
        logger.error(f"SQLite restore failed: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Database restore script")
    parser.add_argument("backup_file", help="Backup file to restore from")
    parser.add_argument("--list", action="store_true", help="List available backups")
    parser.add_argument("--database-url", help="Override database URL")

    args = parser.parse_args()

    # Get database URL
    database_url = args.database_url or get_database_url()
    if not database_url:
        logger.error("No database URL provided")
        sys.exit(1)

    backup_dir = Path("backups")

    if args.list:
        # List available backups
        backups = list_backups(backup_dir)
        if backups:
            print("Available backups:")
            for backup in backups:
                print(f"  {backup['filename']} ({backup['size']} bytes)")
        else:
            print("No backups found")
        return

    # Check if backup file exists
    backup_path = Path(args.backup_file)
    if not backup_path.is_absolute():
        backup_path = backup_dir / backup_path

    if not backup_path.exists():
        logger.error(f"Backup file not found: {backup_path}")
        sys.exit(1)

    # Confirm restore
    print(f"WARNING: This will overwrite the current database with {backup_path}")
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != "yes":
        logger.info("Restore cancelled")
        sys.exit(0)

    # Perform restore
    if database_url.startswith("postgresql://"):
        success = restore_postgresql(database_url, backup_path)
    elif database_url.startswith("sqlite://"):
        success = restore_sqlite(database_url, backup_path)
    else:
        logger.error(f"Unsupported database type: {database_url}")
        sys.exit(1)

    if success:
        logger.info("Database restore completed successfully")
        sys.exit(0)
    else:
        logger.error("Database restore failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
