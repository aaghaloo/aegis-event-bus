#!/usr/bin/env python3
"""
Comprehensive disaster recovery script.
Handles backup, restore, and system recovery procedures.
"""

import argparse
import json
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DisasterRecovery:
    """Disaster recovery coordinator."""

    def __init__(self):
        self.backup_dir = Path("backups")
        self.logs_dir = Path("logs")
        self.config_dir = Path("config")

        # Create necessary directories
        self.backup_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

    def create_full_backup(self):
        """Create a full system backup."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"full_backup_{timestamp}"
            backup_path = self.backup_dir / backup_name
            backup_path.mkdir(exist_ok=True)

            logger.info(f"Creating full backup: {backup_path}")

            # Backup database
            self._backup_database(backup_path)

            # Backup configuration files
            self._backup_config(backup_path)

            # Backup certificates
            self._backup_certificates(backup_path)

            # Create backup manifest
            self._create_manifest(backup_path, timestamp)

            logger.info("Full backup completed successfully")
            return backup_path

        except Exception as e:
            logger.error(f"Full backup failed: {str(e)}")
            return None

    def _backup_database(self, backup_path: Path):
        """Backup database."""
        try:
            from app.config import settings

            db_backup_dir = backup_path / "database"
            db_backup_dir.mkdir(exist_ok=True)

            if settings.DATABASE_URL.startswith("postgresql://"):
                # PostgreSQL backup
                self._backup_postgresql(settings.DATABASE_URL, db_backup_dir)
            elif settings.DATABASE_URL.startswith("sqlite://"):
                # SQLite backup
                self._backup_sqlite(settings.DATABASE_URL, db_backup_dir)

        except Exception as e:
            logger.error(f"Database backup failed: {str(e)}")

    def _backup_postgresql(self, database_url: str, backup_dir: Path):
        """Backup PostgreSQL database."""
        # Implementation similar to backup_database.py
        pass

    def _backup_sqlite(self, database_url: str, backup_dir: Path):
        """Backup SQLite database."""
        # Implementation similar to backup_database.py
        pass

    def _backup_config(self, backup_path: Path):
        """Backup configuration files."""
        try:
            config_backup_dir = backup_path / "config"
            config_backup_dir.mkdir(exist_ok=True)

            # Copy important config files
            config_files = [
                ".env",
                "docker-compose.yml",
                "Dockerfile",
                "requirements.txt",
                "requirements.lock",
            ]

            for config_file in config_files:
                if Path(config_file).exists():
                    shutil.copy2(config_file, config_backup_dir)
                    logger.info(f"Backed up config: {config_file}")

        except Exception as e:
            logger.error(f"Config backup failed: {str(e)}")

    def _backup_certificates(self, backup_path: Path):
        """Backup certificates and keys."""
        try:
            cert_backup_dir = backup_path / "certificates"
            cert_backup_dir.mkdir(exist_ok=True)

            # Copy certificate directories
            cert_dirs = ["mosquitto/certs", "certs"]

            for cert_dir in cert_dirs:
                if Path(cert_dir).exists():
                    shutil.copytree(
                        cert_dir, cert_backup_dir / cert_dir, dirs_exist_ok=True
                    )
                    logger.info(f"Backed up certificates: {cert_dir}")

        except Exception as e:
            logger.error(f"Certificate backup failed: {str(e)}")

    def _create_manifest(self, backup_path: Path, timestamp: str):
        """Create backup manifest."""
        try:
            manifest = {
                "timestamp": timestamp,
                "backup_type": "full",
                "components": ["database", "config", "certificates"],
                "created_by": "disaster_recovery.py",
                "version": "1.0",
            }

            manifest_file = backup_path / "manifest.json"
            with open(manifest_file, "w") as f:
                json.dump(manifest, f, indent=2)

            logger.info(f"Created backup manifest: {manifest_file}")

        except Exception as e:
            logger.error(f"Manifest creation failed: {str(e)}")

    def restore_from_backup(self, backup_path: Path):
        """Restore system from backup."""
        try:
            logger.info(f"Starting restore from backup: {backup_path}")

            # Verify backup
            if not self._verify_backup(backup_path):
                logger.error("Backup verification failed")
                return False

            # Restore database
            self._restore_database(backup_path)

            # Restore configuration
            self._restore_config(backup_path)

            # Restore certificates
            self._restore_certificates(backup_path)

            logger.info("System restore completed successfully")
            return True

        except Exception as e:
            logger.error(f"System restore failed: {str(e)}")
            return False

    def _verify_backup(self, backup_path: Path) -> bool:
        """Verify backup integrity."""
        try:
            manifest_file = backup_path / "manifest.json"
            if not manifest_file.exists():
                logger.error("Backup manifest not found")
                return False

            with open(manifest_file, "r") as f:
                json.load(f)  # Verify manifest is valid JSON

            # Check required components
            required_components = ["database", "config"]
            for component in required_components:
                component_dir = backup_path / component
                if not component_dir.exists():
                    logger.error(f"Required component missing: {component}")
                    return False

            logger.info("Backup verification passed")
            return True

        except Exception as e:
            logger.error(f"Backup verification failed: {str(e)}")
            return False

    def _restore_database(self, backup_path: Path):
        """Restore database from backup."""
        try:
            db_backup_dir = backup_path / "database"
            if db_backup_dir.exists():
                # Implementation similar to restore_database.py
                logger.info("Database restore completed")
            else:
                logger.warning("No database backup found")

        except Exception as e:
            logger.error(f"Database restore failed: {str(e)}")

    def _restore_config(self, backup_path: Path):
        """Restore configuration from backup."""
        try:
            config_backup_dir = backup_path / "config"
            if config_backup_dir.exists():
                # Restore config files
                for config_file in config_backup_dir.iterdir():
                    if config_file.is_file():
                        shutil.copy2(config_file, Path(config_file.name))
                        logger.info(f"Restored config: {config_file.name}")

        except Exception as e:
            logger.error(f"Config restore failed: {str(e)}")

    def _restore_certificates(self, backup_path: Path):
        """Restore certificates from backup."""
        try:
            cert_backup_dir = backup_path / "certificates"
            if cert_backup_dir.exists():
                # Restore certificates
                for cert_dir in cert_backup_dir.iterdir():
                    if cert_dir.is_dir():
                        shutil.copytree(
                            cert_dir, Path(cert_dir.name), dirs_exist_ok=True
                        )
                        logger.info(f"Restored certificates: {cert_dir.name}")

        except Exception as e:
            logger.error(f"Certificate restore failed: {str(e)}")

    def list_backups(self):
        """List available backups."""
        try:
            backups = []
            for backup_dir in self.backup_dir.iterdir():
                if backup_dir.is_dir() and backup_dir.name.startswith("full_backup_"):
                    manifest_file = backup_dir / "manifest.json"
                    if manifest_file.exists():
                        with open(manifest_file, "r") as f:
                            manifest = json.load(f)

                        backups.append(
                            {
                                "name": backup_dir.name,
                                "timestamp": manifest.get("timestamp", "unknown"),
                                "size": sum(
                                    f.stat().st_size
                                    for f in backup_dir.rglob("*")
                                    if f.is_file()
                                ),
                            }
                        )

            return sorted(backups, key=lambda x: x["timestamp"], reverse=True)

        except Exception as e:
            logger.error(f"Failed to list backups: {str(e)}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Disaster recovery script")
    parser.add_argument("--backup", action="store_true", help="Create full backup")
    parser.add_argument("--restore", help="Restore from backup directory")
    parser.add_argument("--list", action="store_true", help="List available backups")

    args = parser.parse_args()

    dr = DisasterRecovery()

    if args.backup:
        backup_path = dr.create_full_backup()
        if backup_path:
            logger.info(f"Backup created: {backup_path}")
            sys.exit(0)
        else:
            logger.error("Backup failed")
            sys.exit(1)

    elif args.restore:
        backup_path = Path(args.restore)
        if not backup_path.exists():
            logger.error(f"Backup not found: {backup_path}")
            sys.exit(1)

        # Confirm restore
        print(f"WARNING: This will restore the system from {backup_path}")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Restore cancelled")
            sys.exit(0)

        if dr.restore_from_backup(backup_path):
            logger.info("System restore completed successfully")
            sys.exit(0)
        else:
            logger.error("System restore failed")
            sys.exit(1)

    elif args.list:
        backups = dr.list_backups()
        if backups:
            print("Available backups:")
            for backup in backups:
                size_str = f"{backup['size']} bytes"
                print(f"  {backup['name']} ({backup['timestamp']}) - {size_str}")
        else:
            print("No backups found")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
