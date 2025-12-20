from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import timedelta
from jose import jwt, JWTError
import os
from ...models.chat import AuthCheckRequest, AuthCheckResponse
from ...services.auth_service import AuthService, TokenData


router = APIRouter()
security = HTTPBearer()


@router.post("/auth/verify", response_model=AuthCheckResponse)
async def verify_auth(request: AuthCheckRequest):
    """
    Verify if the provided token is valid and user is authenticated.
    """
    auth_status = AuthService.get_authentication_status(request.token)

    if auth_status.status == "authenticated":
        return AuthCheckResponse(
            authenticated=True,
            user_id=auth_status.user_id,
            message="Authentication successful"
        )
    else:
        return AuthCheckResponse(
            authenticated=False,
            user_id=None,
            message="Invalid or expired token"
        )


@router.post("/auth/login")
async def login(username: str, password: str):
    """
    Authenticate user and return JWT token.
    This is a placeholder implementation - in a real system, you'd validate against a database.
    """
    token = AuthService.authenticate_user(username, password)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": token, "token_type": "bearer"}


# Optional: Middleware-style dependency for protecting routes
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[TokenData]:
    """
    Dependency to get current user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("JWT_SECRET_KEY", "your-default-secret-key-change-in-production"), algorithms=[os.getenv("JWT_ALGORITHM", "HS256")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data