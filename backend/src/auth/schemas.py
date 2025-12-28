from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Literal


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        # Ensure password has at least one uppercase, one lowercase, and one digit
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    profile_picture_url: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user responses (excludes sensitive data)"""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    profile_picture_url: Optional[str] = None
    oauth_provider: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserInDB(UserResponse):
    """Schema for user data including password hash (for internal use only)"""
    password_hash: str


# Authentication Schemas
class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: str
    email: EmailStr
    exp: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema for refresh token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    """Schema for authentication response"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Password Reset Schemas
class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordResetVerify(BaseModel):
    """Schema for password reset verification"""
    token: str
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def validate_password(cls, v):
        # Ensure password has at least one uppercase, one lowercase, and one digit
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordResetResponse(BaseModel):
    """Schema for password reset response"""
    message: str = "Password reset successfully"


# OAuth Schemas
class OAuthLoginRequest(BaseModel):
    """Schema for OAuth login request"""
    provider: Literal["google", "github"]
    code: str
    redirect_uri: Optional[str] = None


class OAuthCallbackResponse(BaseModel):
    """Schema for OAuth callback response"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    is_new_user: bool = False


# Remember Me Schema
class RememberMeRequest(BaseModel):
    """Schema for remember me functionality"""
    remember_me: bool = False


# Verification Schemas
class VerifyEmailRequest(BaseModel):
    """Schema for email verification request"""
    token: str


class VerifyEmailResponse(BaseModel):
    """Schema for email verification response"""
    message: str = "Email verified successfully"


class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def validate_password(cls, v):
        # Ensure password has at least one uppercase, one lowercase, and one digit
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class ChangePasswordResponse(BaseModel):
    """Schema for change password response"""
    message: str = "Password changed successfully"