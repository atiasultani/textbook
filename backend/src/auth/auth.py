from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.auth.crud import (
    get_user_by_email, get_user_by_id, create_user, update_user_last_login,
    create_auth_session, get_auth_session_by_refresh_token_hash, deactivate_auth_session,
    create_password_reset_token, get_password_reset_token_by_token_hash, mark_password_reset_token_as_used,
    get_oauth_account_by_provider_and_id, create_oauth_account, link_oauth_account_to_user
)
from src.auth.schemas import UserCreate, TokenData
from src.auth.security import (
    verify_password, get_password_hash, create_tokens, verify_token,
    generate_password_reset_token, hash_refresh_token, verify_refresh_token_hash
)
from datetime import datetime, timedelta


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user with email and password
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_user_with_session(db: Session, user_data: UserCreate, user_agent: Optional[str] = None, ip_address: Optional[str] = None):
    """
    Create a new user and their initial authentication session
    """
    # Create the user
    user = create_user(db, user_data)

    # Create tokens for the user
    tokens = create_tokens(user.id, user.email)

    # Hash the refresh token for secure storage
    refresh_token_hash = hash_refresh_token(tokens["refresh_token"])

    # Calculate expiration times
    access_token_expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes
    refresh_token_expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days

    # Create an authentication session
    auth_session = create_auth_session(
        db,
        user_id=user.id,
        access_token=tokens["access_token"],
        refresh_token_hash=refresh_token_hash,
        access_token_expires_at=access_token_expires_at,
        refresh_token_expires_at=refresh_token_expires_at,
        user_agent=user_agent,
        ip_address=ip_address
    )

    # Update the user's last login time
    update_user_last_login(db, user.id)

    return {
        "user": user,
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }


def refresh_access_token(db: Session, refresh_token: str):
    """
    Refresh an access token using a refresh token
    """
    # Find the authentication session by refresh token hash
    auth_session = get_auth_session_by_refresh_token_hash(db, hash_refresh_token(refresh_token))

    if not auth_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the refresh token is expired
    if auth_session.refresh_token_expires_at < datetime.utcnow():
        # Token is expired, deactivate the session
        deactivate_auth_session(db, auth_session.id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the refresh token
    if not verify_refresh_token_hash(refresh_token, auth_session.refresh_token_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the user
    user = get_user_by_id(db, auth_session.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new tokens
    new_tokens = create_tokens(user.id, user.email)

    # Return new access token
    return {
        "access_token": new_tokens["access_token"],
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }

def initiate_password_reset(db: Session, email: str, ip_address: str, user_agent: str):
    """
    Initiate a password reset process
    """
    user = get_user_by_email(db, email)
    if not user:
        # Prevent email enumeration
        return {"message": "If the email exists, a reset link has been sent"}

    # Generate raw reset token
    reset_token = generate_password_reset_token()

    # Hash before storing
    token_hash = get_password_hash(reset_token)

    expires_at = datetime.utcnow() + timedelta(hours=1)

    create_password_reset_token(
        db,
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )

    # TODO: send email instead of print
    print("🔐 Password Reset Link")
    print(f"http://localhost:5173/reset-password?token={reset_token}")

    return {"message": "If the email exists, a reset link has been sent"}
def reset_user_password(db: Session, token: str, new_password: str):
    """
    Reset a user's password using a reset token
    """

    # Get the most recent valid reset request
    reset_token_record = get_password_reset_token_by_token_hash(db)

    if not reset_token_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    # IMPORTANT: verify instead of hashing again
    if not verify_password(token, reset_token_record.token_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    if reset_token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    if reset_token_record.used_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token already used"
        )

    user = get_user_by_id(db, reset_token_record.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )

    user.password_hash = get_password_hash(new_password)

    mark_password_reset_token_as_used(db, reset_token_record.id)

    return {"message": "Password reset successfully"}


def handle_oauth_login(db: Session, provider: str, provider_account_id: str, email: str, name: str,
                      access_token: str, refresh_token: Optional[str] = None, expires_at: Optional[datetime] = None):
    """
    Handle OAuth login - find/create user and create session
    """
    # Try to find an existing OAuth account
    oauth_account = get_oauth_account_by_provider_and_id(db, provider, provider_account_id)

    if oauth_account:
        # OAuth account exists, check if it's linked to a user
        if oauth_account.user_id:
            # Update the OAuth account with new tokens
            from backend.src.auth.crud import update_oauth_account
            update_oauth_account(
                db,
                oauth_account_id=oauth_account.id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
                name=name
            )

            # Get the user
            user = get_user_by_id(db, oauth_account.user_id)
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is inactive",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Update last login
            update_user_last_login(db, user.id)

            # Create new tokens
            tokens = create_tokens(user.id, user.email)

            return {
                "user": user,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "bearer",
                "is_new_user": False
            }
        else:
            # OAuth account exists but isn't linked to a user - this shouldn't happen in normal flow
            # But if it does, we can create a new user or link to an existing one
            # For now, we'll create a new user
            user_data = UserCreate(name=name, email=email, password=get_password_hash("temp_password_placeholder"))
            user = create_user(db, user_data)

            # Link the OAuth account to the user
            link_oauth_account_to_user(db, oauth_account.id, user.id)

            # Update last login
            update_user_last_login(db, user.id)

            # Create new tokens
            tokens = create_tokens(user.id, user.email)

            return {
                "user": user,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "bearer",
                "is_new_user": True
            }
    else:
        # OAuth account doesn't exist, create a new one
        # First, check if a user with this email already exists
        existing_user = get_user_by_email(db, email)

        if existing_user:
            # User already exists, link the OAuth account to the existing user
            oauth_account = create_oauth_account(
                db,
                user_id=existing_user.id,
                provider=provider,
                provider_account_id=provider_account_id,
                email=email,
                name=name,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at
            )

            # Update last login
            update_user_last_login(db, existing_user.id)

            # Create new tokens
            tokens = create_tokens(existing_user.id, existing_user.email)

            return {
                "user": existing_user,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "bearer",
                "is_new_user": False
            }
        else:
            # User doesn't exist, create a new user
            user_data = UserCreate(name=name, email=email, password=get_password_hash("temp_password_placeholder"))
            user = create_user(db, user_data)

            # Create the OAuth account and link it to the new user
            create_oauth_account(
                db,
                user_id=user.id,
                provider=provider,
                provider_account_id=provider_account_id,
                email=email,
                name=name,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at
            )

            # Update last login
            update_user_last_login(db, user.id)

            # Create new tokens
            tokens = create_tokens(user.id, user.email)

            return {
                "user": user,
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "token_type": "bearer",
                "is_new_user": True
            }


def verify_access_token(db: Session, token: str) -> Optional[TokenData]:
    """
    Verify an access token and return user information
    """
    payload = verify_token(token)
    if payload is None:
        return None

    # Check if token type is access token
    token_type = payload.get("type")
    if token_type != "access":
        return None

    # Check if token is expired
    exp_timestamp = payload.get("exp")
    if not exp_timestamp:
        return None

    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    if datetime.utcnow() > exp_datetime:
        return None

    # Check if user exists and is active
    user = get_user_by_id(db, payload.get("user_id"))
    if not user or not user.is_active:
        return None

    return TokenData(
        user_id=payload.get("user_id"),
        email=payload.get("email"),
        exp=datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None
    )


def logout_user(db: Session, access_token: str) -> bool:
    """
    Logout a user by invalidating their session
    """
    from backend.src.auth.crud import get_auth_session_by_access_token

    # Find the authentication session by access token
    auth_session = get_auth_session_by_access_token(db, access_token)

    if not auth_session:
        return False

    # Deactivate the session
    return deactivate_auth_session(db, auth_session.id)