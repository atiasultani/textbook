from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    Represents a registered user with attributes including ID, name, email, password hash,
    account status, creation date, and last login time
    """
    id: str
    name: str
    email: EmailStr
    password_hash: str
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    profile_picture_url: Optional[str] = None
    oauth_provider: Optional[str] = None


class AuthenticationSession(BaseModel):
    """
    Represents an active user session with JWT access token, refresh token,
    expiration times, and associated user ID
    """
    id: str
    user_id: str
    access_token: str
    refresh_token_hash: str
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime
    created_at: datetime
    last_used_at: datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    is_active: bool = True


class PasswordResetToken(BaseModel):
    """
    Represents a temporary token for password reset functionality
    with expiration time and associated user
    """
    id: str
    user_id: str
    token_hash: str
    expires_at: datetime
    used_at: Optional[datetime] = None
    created_at: datetime
    ip_address: str
    user_agent: str


class OAuthAccount(BaseModel):
    """
    Represents an OAuth connection for a user (Google, GitHub, etc.)
    """
    id: str
    user_id: str
    provider: str
    provider_account_id: str
    email: EmailStr
    name: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime