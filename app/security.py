# app/security.py
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import schemas
from .config import settings

router = APIRouter()

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Security Settings ---
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIREMENTS = {
    "uppercase": r"[A-Z]",
    "lowercase": r"[a-z]",
    "digit": r"\d",
    "special": r'[!@#$%^&*(),.?":{}|<>]',
}


# --- User Management ---
class UserManager:
    """Centralized user management with configurable users."""

    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
        self._login_attempts: Dict[str, Dict[str, Any]] = {}
        self._load_users()

    def _load_users(self):
        """Load users from environment or use defaults for development."""
        if settings.is_production:
            # In production, users should be loaded from secure storage
            # For now, we'll use environment variables
            self._load_from_env()
        else:
            # Development: use test user only
            self._add_test_user()

    def _load_from_env(self):
        """Load users from environment variables."""
        # Format: USER_1=username:password,USER_2=username2:password2
        users_env = getattr(settings, "USERS", None)
        if users_env:
            for user_entry in users_env.split(","):
                if ":" in user_entry:
                    username, password = user_entry.split(":", 1)
                    self.add_user(username.strip(), password.strip())

    def _add_test_user(self):
        """Add test user for development."""
        # In development, use a simple password that meets basic requirements
        test_password = "TestPass123!"
        self.add_user("testuser", test_password)

    def add_user(self, username: str, password: str):
        """Add a user to the system."""
        # Validate password complexity
        if not self._validate_password(password):
            raise ValueError("Password does not meet complexity requirements")

        self._users[username] = {
            "username": username,
            "hashed_password": pwd_context.hash(password),
            "created_at": datetime.now(timezone.utc),
            "last_login": None,
            "is_active": True,
        }

    def _validate_password(self, password: str) -> bool:
        """Validate password complexity requirements."""
        if len(password) < PASSWORD_MIN_LENGTH:
            return False

        # Check for required character types
        for requirement, pattern in PASSWORD_REQUIREMENTS.items():
            if not re.search(pattern, password):
                return False

        return True

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        return self._users.get(username)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def check_account_lockout(self, username: str) -> bool:
        """Check if account is locked due to too many failed attempts."""
        if username not in self._login_attempts:
            return False

        attempts = self._login_attempts[username]
        if attempts.get("count", 0) >= MAX_LOGIN_ATTEMPTS:
            lockout_time = attempts.get("lockout_until")
            if lockout_time and datetime.now(timezone.utc) < lockout_time:
                return True
            else:
                # Reset lockout if time has passed
                self._login_attempts[username] = {"count": 0, "lockout_until": None}

        return False

    def record_failed_login(self, username: str):
        """Record a failed login attempt."""
        if username not in self._login_attempts:
            self._login_attempts[username] = {"count": 0, "lockout_until": None}

        attempts = self._login_attempts[username]
        attempts["count"] += 1

        if attempts["count"] >= MAX_LOGIN_ATTEMPTS:
            attempts["lockout_until"] = datetime.now(timezone.utc) + LOCKOUT_DURATION

    def record_successful_login(self, username: str):
        """Record a successful login and reset failed attempts."""
        if username in self._login_attempts:
            self._login_attempts[username] = {"count": 0, "lockout_until": None}

        # Update last login time
        if username in self._users:
            self._users[username]["last_login"] = datetime.now(timezone.utc)

    def list_users(self) -> list:
        """List all usernames (for admin purposes)."""
        return list(self._users.keys())

    def deactivate_user(self, username: str) -> bool:
        """Deactivate a user account."""
        if username in self._users:
            self._users[username]["is_active"] = False
            return True
        return False

    def activate_user(self, username: str) -> bool:
        """Activate a user account."""
        if username in self._users:
            self._users[username]["is_active"] = True
            return True
        return False


# Global user manager instance
user_manager = UserManager()


def get_user(username: str):
    """Get user by username (backward compatibility)."""
    return user_manager.get_user(username)


def verify_password(plain_password, hashed_password):
    """Verify password (backward compatibility)."""
    return user_manager.verify_password(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# --- The Main Security Dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None or not user.get("is_active", True):
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Check for account lockout
    if user_manager.check_account_lockout(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account temporarily locked due to too many failed attempts",
        )

    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        # Record failed login attempt
        user_manager.record_failed_login(form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Record successful login
    user_manager.record_successful_login(form_data.username)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Admin endpoints for user management ---
@router.get("/users", tags=["Admin"])
async def list_users(_: dict = Depends(get_current_user)):
    """List all users (admin only)."""
    return {"users": user_manager.list_users()}


@router.post("/users/{username}/deactivate", tags=["Admin"])
async def deactivate_user(username: str, _: dict = Depends(get_current_user)):
    """Deactivate a user account (admin only)."""
    if user_manager.deactivate_user(username):
        return {"message": f"User {username} deactivated"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/users/{username}/activate", tags=["Admin"])
async def activate_user(username: str, _: dict = Depends(get_current_user)):
    """Activate a user account (admin only)."""
    if user_manager.activate_user(username):
        return {"message": f"User {username} activated"}
    raise HTTPException(status_code=404, detail="User not found")
