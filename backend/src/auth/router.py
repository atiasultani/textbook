from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from src.database import get_db
from src.auth.schemas import UserCreate, UserLogin, RefreshTokenRequest, RefreshTokenResponse, AuthResponse, PasswordResetRequest, PasswordResetVerify, OAuthLoginRequest, OAuthCallbackResponse
from src.auth.auth import authenticate_user, create_user_with_session, refresh_access_token, initiate_password_reset, reset_user_password
from src.auth.security import verify_token
from src.auth.oauth import handle_google_oauth_login, handle_github_oauth_login, get_oauth_authorization_url
import os


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
async def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    from backend.src.auth.crud import get_user_by_email
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Get user agent and IP address for session tracking
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host

    # Create user with session
    result = create_user_with_session(db, user_data, user_agent, ip_address)

    return {
        "user": result["user"],
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": result["token_type"]
    }


@router.post("/login", response_model=AuthResponse)
async def login(user_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    Authenticate user and return tokens
    """
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    from backend.src.auth.crud import update_user_last_login
    update_user_last_login(db, user.id)

    # Create tokens
    from backend.src.auth.security import create_tokens
    tokens = create_tokens(user.id, user.email)

    # Create auth session
    from backend.src.auth.security import hash_refresh_token
    from datetime import datetime, timedelta
    refresh_token_hash = hash_refresh_token(tokens["refresh_token"])

    access_token_expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes
    refresh_token_expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days

    from backend.src.auth.crud import create_auth_session
    create_auth_session(
        db,
        user_id=user.id,
        access_token=tokens["access_token"],
        refresh_token_hash=refresh_token_hash,
        access_token_expires_at=access_token_expires_at,
        refresh_token_expires_at=refresh_token_expires_at,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host
    )

    return {
        "user": user,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    result = refresh_access_token(db, refresh_request.refresh_token)
    return result


@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """
    Logout user and invalidate session
    """
    # Get the access token from the authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_header[7:]  # Remove "Bearer " prefix

    # Logout the user
    from backend.src.auth.auth import logout_user
    success = logout_user(db, access_token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Get current user information
    """
    # Get the access token from the authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_header[7:]  # Remove "Bearer " prefix

    # Verify the token and get user info
    from backend.src.auth.auth import verify_access_token
    token_data = verify_access_token(db, access_token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    from backend.src.auth.crud import get_user_by_id
    user = get_user_by_id(db, token_data.user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user": user}


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, req: Request, db: Session = Depends(get_db)):
    """
    Initiate password reset process
    """
    result = initiate_password_reset(
        db,
        request.email,
        req.client.host,
        req.headers.get("user-agent")
    )
    return result


@router.post("/reset-password")
async def reset_password(request: PasswordResetVerify, db: Session = Depends(get_db)):
    """
    Reset user password using reset token
    """
    result = reset_user_password(db, request.token, request.new_password)
    return result


@router.post("/oauth/{provider}/login")
async def oauth_login(provider: str, request: OAuthLoginRequest, db: Session = Depends(get_db)):
    """
    Initiate OAuth login flow
    """
    if provider not in ["google", "github"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )

    authorization_url = get_oauth_authorization_url(
        provider=provider,
        redirect_uri=request.redirect_uri
    )

    return {"authorization_url": authorization_url}


@router.post("/oauth/{provider}/callback", response_model=OAuthCallbackResponse)
async def oauth_callback(provider: str, request: Request, db: Session = Depends(get_db)):
    """
    Handle OAuth callback and authenticate user
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )

    redirect_uri = request.query_params.get("redirect_uri", str(request.url))

    if provider == "google":
        result = await handle_google_oauth_login(db, code, redirect_uri)
    elif provider == "github":
        result = await handle_github_oauth_login(db, code, redirect_uri)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported OAuth provider"
        )

    return result