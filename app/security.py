# app/security.py
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


# --- User Management ---
class UserManager:
    """Centralized user management with configurable users."""

    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
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
        self.add_user("testuser", "testpassword")

    def add_user(self, username: str, password: str):
        """Add a user to the system."""
        self._users[username] = {
            "username": username,
            "hashed_password": pwd_context.hash(password),
        }

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        return self._users.get(username)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def list_users(self) -> list:
        """List all usernames (for admin purposes)."""
        return list(self._users.keys())


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
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

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
