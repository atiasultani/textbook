from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import httpx
from src.auth.auth import handle_oauth_login
from src.auth.crud import get_oauth_account_by_provider_and_id, create_oauth_account
from src.auth.security import SECRET_KEY, ALGORITHM
from jose import jwt
import os

# OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


async def get_google_user_info(access_token: str) -> dict:
    """
    Get user info from Google using the access token
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to fetch user info from Google"
            )
        return response.json()


async def get_github_user_info(access_token: str) -> dict:
    """
    Get user info from GitHub using the access token
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to fetch user info from GitHub"
            )
        user_data = response.json()

        # Also get email if it's not public
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
        )
        if email_response.status_code == 200:
            emails = email_response.json()
            primary_email = next((email for email in emails if email.get("primary", False)), None)
            if primary_email:
                user_data["email"] = primary_email["email"]

        return user_data


async def exchange_code_for_token(provider: str, code: str, redirect_uri: str) -> dict:
    """
    Exchange authorization code for access token
    """
    if provider == "google":
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
    elif provider == "github":
        token_url = "https://github.com/login/oauth/access_token"
        data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect_uri
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )

    if not data["client_id"] or not data["client_secret"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth credentials not configured for {provider}"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to exchange code for token with {provider}"
            )

        token_data = response.json()
        if provider == "github":
            # GitHub returns token in query string format, need to parse it
            if "access_token" not in token_data:
                # If it's a query string, parse it
                import urllib.parse
                parsed = urllib.parse.parse_qs(response.text)
                access_token = parsed.get("access_token", [None])[0]
                if not access_token:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Failed to get access token from GitHub"
                    )
                token_data = {"access_token": access_token}

        return token_data


async def handle_google_oauth_login(db: Session, code: str, redirect_uri: str):
    """
    Handle Google OAuth login flow
    """
    # Exchange code for token
    token_data = await exchange_code_for_token("google", code, redirect_uri)
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get access token from Google"
        )

    # Get user info from Google
    user_info = await get_google_user_info(access_token)

    # Extract user data
    provider_account_id = user_info.get("id")
    email = user_info.get("email")
    name = user_info.get("name") or user_info.get("given_name", "")

    # Handle the OAuth login (find/create user and session)
    return handle_oauth_login(
        db=db,
        provider="google",
        provider_account_id=provider_account_id,
        email=email,
        name=name,
        access_token=access_token,
        refresh_token=token_data.get("refresh_token"),
        expires_at=datetime.fromtimestamp(token_data.get("expires_at", 0)) if token_data.get("expires_at") else None
    )


async def handle_github_oauth_login(db: Session, code: str, redirect_uri: str):
    """
    Handle GitHub OAuth login flow
    """
    # Exchange code for token
    token_data = await exchange_code_for_token("github", code, redirect_uri)
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get access token from GitHub"
        )

    # Get user info from GitHub
    user_info = await get_github_user_info(access_token)

    # Extract user data
    provider_account_id = str(user_info.get("id"))
    email = user_info.get("email") or ""
    name = user_info.get("name") or user_info.get("login", "")

    # Handle the OAuth login (find/create user and session)
    return handle_oauth_login(
        db=db,
        provider="github",
        provider_account_id=provider_account_id,
        email=email,
        name=name,
        access_token=access_token,
        refresh_token=token_data.get("refresh_token"),
        expires_at=None  # GitHub doesn't return expiration by default
    )


def get_oauth_authorization_url(provider: str, redirect_uri: str = None) -> str:
    """
    Generate OAuth authorization URL for the specified provider
    """
    if provider == "google":
        if not GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google OAuth not configured"
            )

        auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri or f'{FRONTEND_URL}/auth/callback/google'}&response_type=code&scope=openid%20email%20profile&access_type=offline"
        return auth_url

    elif provider == "github":
        if not GITHUB_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GitHub OAuth not configured"
            )

        auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri or f'{FRONTEND_URL}/auth/callback/github'}&scope=user:email"
        return auth_url

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}"
        )