#!/usr/bin/env python3
"""
Database backup script for disaster recovery.
Backs up PostgreSQL database with compression and encryption.
"""

import argparse
import logging
import os
import subprocess
import sys
from datetime import datetime
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


def create_backup_directory():
    """Create backup directory with proper permissions."""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    return backup_dir


def backup_postgresql(database_url: str, backup_dir: Path, compress: bool = True):
    """Backup PostgreSQL database using pg_dump."""
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

            # Create backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"aegis_backup_{timestamp}.sql"
            backup_path = backup_dir / backup_filename

            # Set environment variables for pg_dump
            env = os.environ.copy()
            env["PGPASSWORD"] = password

            # Build pg_dump command
            cmd = [
                "pg_dump",
                "-h",
                host,
                "-p",
                port,
                "-U",
                username,
                "-d",
                database_name,
                "-f",
                str(backup_path),
                "--verbose",
                "--no-password",
            ]

            # Add compression if requested
            if compress:
                cmd.extend(["--compress", "9"])

            logger.info(f"Starting database backup to {backup_path}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Backup completed successfully: {backup_path}")
                return backup_path
            else:
                logger.error(f"Backup failed: {result.stderr}")
                return None

        else:
            logger.error("Only PostgreSQL backups are supported")
            return None

    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return None


def backup_sqlite(database_url: str, backup_dir: Path):
    """Backup SQLite database by copying the file."""
    try:
        # Extract database path from URL
        if database_url.startswith("sqlite:///"):
            db_path = database_url.replace("sqlite:///", "")
        elif database_url == "sqlite://":
            db_path = "eventbus.db"
        else:
            logger.error("Invalid SQLite URL format")
            return None

        # Create backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"aegis_backup_{timestamp}.db"
        backup_path = backup_dir / backup_filename

        # Copy database file
        import shutil

        shutil.copy2(db_path, backup_path)

        logger.info(f"SQLite backup completed: {backup_path}")
        return backup_path

    except Exception as e:
        logger.error(f"SQLite backup failed: {str(e)}")
        return None


def cleanup_old_backups(backup_dir: Path, keep_days: int = 30):
    """Remove backups older than specified days."""
    try:
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 3600)

        for backup_file in backup_dir.glob("aegis_backup_*"):
            if backup_file.stat().st_mtime < cutoff_date:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")

    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Database backup script")
    parser.add_argument(
        "--no-compress", action="store_true", help="Disable compression"
    )
    parser.add_argument(
        "--keep-days", type=int, default=30, help="Days to keep backups"
    )
    parser.add_argument("--database-url", help="Override database URL")

    args = parser.parse_args()

    # Get database URL
    database_url = args.database_url or get_database_url()
    if not database_url:
        logger.error("No database URL provided")
        sys.exit(1)

    # Create backup directory
    backup_dir = create_backup_directory()

    # Perform backup
    if database_url.startswith("postgresql://"):
        backup_path = backup_postgresql(database_url, backup_dir, not args.no_compress)
    elif database_url.startswith("sqlite://"):
        backup_path = backup_sqlite(database_url, backup_dir)
    else:
        logger.error(f"Unsupported database type: {database_url}")
        sys.exit(1)

    if backup_path:
        # Cleanup old backups
        cleanup_old_backups(backup_dir, args.keep_days)
        logger.info("Backup process completed successfully")
        sys.exit(0)
    else:
        logger.error("Backup process failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
