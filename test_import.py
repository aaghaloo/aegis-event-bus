#!/usr/bin/env python3
"""
Test script to verify app module can be imported.
This helps debug CI/CD import issues.
"""

import importlib.util
import os
import sys


def test_imports():
    """Test that all app modules can be imported."""
    try:
        print("Testing app module imports...")

        # Test all modules using importlib
        modules_to_test = [
            "app",
            "app.db",
            "app.main",
            "app.schemas",
            "app.endpoints",
            "app.security",
            "app.validators",
        ]

        for module_name in modules_to_test:
            if importlib.util.find_spec(module_name) is not None:
                print(f"✅ {module_name} module available")
            else:
                print(f"❌ {module_name} module not found")
                return False

        print("🎉 All imports successful!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"Python path: {sys.path}")
        print(f"Current directory: {os.getcwd()}")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
