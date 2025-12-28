from datetime import datetime, timedelta
from typing import Optional
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# Security schemes
security_scheme = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plain password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token with expiration
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new refresh token with expiration
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user_payload(credentials: HTTPAuthorizationCredentials = security_scheme) -> Optional[dict]:
    """
    Get the current user's payload from the authorization header
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if token type is access token
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def hash_refresh_token(refresh_token: str) -> str:
    """
    Hash a refresh token for secure storage
    """
    return get_password_hash(refresh_token)


def verify_refresh_token_hash(token: str, hashed_token: str) -> bool:
    """
    Verify a refresh token against its hash
    """
    return verify_password(token, hashed_token)


def generate_verification_token() -> str:
    """
    Generate a random verification token
    """
    return secrets.token_urlsafe(32)


def generate_password_reset_token() -> str:
    """
    Generate a random password reset token
    """
    return secrets.token_urlsafe(32)


def create_tokens(user_id: str, email: str) -> dict:
    """
    Create both access and refresh tokens for a user
    """
    access_token = create_access_token(data={"user_id": user_id, "email": email})
    refresh_token = create_refresh_token(data={"user_id": user_id, "email": email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def is_token_expired(payload: dict) -> bool:
    """
    Check if a token is expired based on its 'exp' claim
    """
    exp_timestamp = payload.get("exp")
    if not exp_timestamp:
        return True

    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    return datetime.utcnow() > exp_datetime


def get_token_expires_in(payload: dict) -> int:
    """
    Get the number of seconds until token expiration
    """
    exp_timestamp = payload.get("exp")
    if not exp_timestamp:
        return 0

    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    seconds_until_expiry = (exp_datetime - datetime.utcnow()).total_seconds()
    return int(seconds_until_expiry) if seconds_until_expiry > 0 else 0