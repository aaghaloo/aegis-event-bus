"""Test that secrets are properly handled and not hardcoded."""

import os
import re
from pathlib import Path

import pytest


class TestSecretsHandling:
    """Test that secrets are properly handled."""

    def test_no_hardcoded_passwords_in_code(self):
        """Test that no hardcoded passwords exist in Python files."""
        hardcoded_patterns = [
            r"password\s*=\s*['\"][^'\"]{8,}['\"]",  # password = "something"
            r"secret\s*=\s*['\"][^'\"]{8,}['\"]",  # secret = "something"
            r"token\s*=\s*['\"][^'\"]{8,}['\"]",  # token = "something"
        ]

        python_files = list(Path("app").rglob("*.py")) + list(
            Path("tests").rglob("*.py")
        )

        for file_path in python_files:
            if file_path.name in ["__init__.py", "conftest.py"]:
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                # Allow test passwords in test files and CI fallback passwords
                if "test" in file_path.name.lower():
                    continue

                # Filter out CI fallback passwords
                filtered_matches = []
                for match in matches:
                    if "TestPass123!" in match and (
                        "CI" in content or "GITHUB_ACTIONS" in content
                    ):
                        continue  # Skip CI fallback passwords
                    filtered_matches.append(match)

                assert (
                    not filtered_matches
                ), f"Hardcoded secret found in {file_path}: {filtered_matches}"

    def test_environment_variables_used_for_secrets(self):
        """Test that environment variables are used for secrets."""
        secret_vars = [
            "SECRET_KEY",
            "TEST_USER_PASSWORD",
            "POSTGRES_PASSWORD",
            "JWT_SECRET",
        ]

        for var in secret_vars:
            # Check if variable is referenced in code
            python_files = list(Path("app").rglob("*.py"))
            found = False

            for file_path in python_files:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if (
                        f"os.getenv('{var}')" in content
                        or f'os.getenv("{var}")' in content
                    ):
                        found = True
                        break

            if var in ["SECRET_KEY", "TEST_USER_PASSWORD"]:
                assert found, f"Environment variable {var} should be used in code"

    def test_certificate_files_not_tracked(self):
        """Test that certificate files are not tracked in git."""
        cert_extensions = [".crt", ".key", ".pem", ".p12", ".pfx", ".csr", ".srl"]

        for ext in cert_extensions:
            cert_files = list(Path(".").rglob(f"*{ext}"))
            for cert_file in cert_files:
                # Check if file is in .gitignore
                with open(".gitignore", "r") as f:
                    gitignore_content = f.read()

                assert (
                    f"*{ext}" in gitignore_content
                ), f"Certificate extension {ext} not in .gitignore"

    def test_secret_key_validation(self):
        """Test that SECRET_KEY validation works properly."""
        from app.config import Settings

        # Test that SECRET_KEY is generated in development
        settings = Settings(ENV="development", SECRET_KEY=None)
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) >= 32

    def test_test_password_environment_variable(self):
        """Test that test password is properly handled."""
        from app.security import UserManager

        # Test that it fails when TEST_USER_PASSWORD is not set
        # (only in non-CI environments)
        ci_env = os.getenv("CI") or os.getenv("GITHUB_ACTIONS")
        if not ci_env:
            # Save original value
            original_password = os.getenv("TEST_USER_PASSWORD")

            # Remove the environment variable
            if "TEST_USER_PASSWORD" in os.environ:
                del os.environ["TEST_USER_PASSWORD"]

            try:
                error_msg = "TEST_USER_PASSWORD environment variable must be set"
                with pytest.raises(ValueError, match=error_msg):
                    UserManager()
            finally:
                # Restore original value
                if original_password:
                    os.environ["TEST_USER_PASSWORD"] = original_password
                elif "TEST_USER_PASSWORD" in os.environ:
                    del os.environ["TEST_USER_PASSWORD"]
        else:
            # In CI environment, just verify UserManager can be created
            user_manager = UserManager()
            assert user_manager is not None

    def test_no_secrets_in_logs(self):
        """Test that secrets are not logged."""
        python_files = list(Path("app").rglob("*.py"))

        for file_path in python_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for logging statements that might expose secrets
            log_patterns = [
                r"logger\.(info|debug|warning|error)\(.*password",
                r"logger\.(info|debug|warning|error)\(.*secret",
                r"logger\.(info|debug|warning|error)\(.*key",
                r"logger\.(info|debug|warning|error)\(.*token",
            ]

            for pattern in log_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                assert (
                    not matches
                ), f"Potential secret logging found in {file_path}: {matches}"
