from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from ..models.chat import AuthenticationStatus, AuthenticationStatusEnum


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class TokenData(BaseModel):
    username: Optional[str] = None


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a plain password."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[TokenData]:
        """Verify a JWT token and return token data if valid."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            token_data = TokenData(username=username)
            return token_data
        except JWTError:
            return None

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[str]:
        """
        Authenticate a user by username and password.
        This is a placeholder implementation - in a real system, you'd check against a database.
        """
        # In a real implementation, you would:
        # 1. Look up the user in the database by username
        # 2. Verify the password using verify_password()
        # 3. Return user data if valid, None if not

        # Placeholder implementation for demonstration
        # In a real system, you'd validate against actual user data
        if username and password:  # Simplified check for demo purposes
            return AuthService.create_access_token(data={"sub": username})
        return None

    @staticmethod
    def get_authentication_status(token: Optional[str]) -> AuthenticationStatus:
        """
        Get the authentication status from a token.
        Returns an AuthenticationStatus object with the status and user info.
        """
        if not token:
            return AuthenticationStatus(
                status=AuthenticationStatusEnum.unauthenticated,
                user_id=None,
                token=None,
                expires_at=None
            )

        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        token_data = AuthService.verify_token(token)
        if not token_data or not token_data.username:
            return AuthenticationStatus(
                status=AuthenticationStatusEnum.unauthenticated,
                user_id=None,
                token=token,
                expires_at=None
            )

        # In a real implementation, you'd look up user details in the database
        # For now, we'll use the username as the user_id
        return AuthenticationStatus(
            status=AuthenticationStatusEnum.authenticated,
            user_id=token_data.username,
            token=token,
            expires_at=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )


# Authentication middleware function
async def auth_middleware(request: Request, call_next):
    """
    Middleware to check authentication for protected endpoints.
    """
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif auth_header and auth_header.startswith("Token "):
        token = auth_header[6:]

    # Get authentication status
    auth_status = AuthService.get_authentication_status(token)

    # Store auth status in request state for use in route handlers
    request.state.auth_status = auth_status

    response = await call_next(request)
    return response