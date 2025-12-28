from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.auth.security import verify_token, get_current_user_payload
from src.auth.crud import get_user_by_id
from src.database import get_db
from sqlalchemy.orm import Session
from contextlib import contextmanager
from fastapi.responses import JSONResponse


class AuthMiddleware:
    def __init__(self):
        self.security_scheme = HTTPBearer()

    @contextmanager
    def get_db_session(self):
        """
        Context manager to handle database session
        """
        db = next(get_db())
        try:
            yield db
        finally:
            db.close()

    def verify_token_middleware(self, request: Request) -> dict:
        """
        Verify the token from the request and return the payload
        """
        try:
            credentials: HTTPAuthorizationCredentials = self.security_scheme(request)
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
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception:
            # Handle other exceptions
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_user_middleware(self, request: Request) -> dict:
        """
        Verify the user from the token in the request
        """
        payload = self.verify_token_middleware(request)

        with self.get_db_session() as db:
            user = get_user_by_id(db, payload.get("user_id"))
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is inactive or does not exist",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return {
            "user": user,
            "payload": payload
        }

    async def __call__(self, request: Request, call_next):
        """
        ASGI middleware to validate tokens for all requests
        """
        # Define paths that don't require authentication
        public_paths = ["/auth/login", "/auth/register", "/auth/refresh", "/auth/forgot-password", "/auth/reset-password", "/docs", "/redoc", "/openapi.json"]

        # Check if the path is public
        is_public = any(request.url.path.startswith(path) for path in public_paths)

        if is_public:
            # Skip authentication for public paths
            response = await call_next(request)
            return response

        # For protected paths, validate the token
        try:
            payload = self.verify_token_middleware(request)

            # Add user info to request state for later use
            with self.get_db_session() as db:
                user = get_user_by_id(db, payload.get("user_id"))
                if not user or not user.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User account is inactive or does not exist",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                # Add user information to request state
                request.state.user = user
                request.state.auth_status = "authenticated"

        except HTTPException as e:
            # Return JSON response for unauthorized access
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers=e.headers
            )
        except Exception:
            # Return generic error for other issues
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Unauthorized"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Continue with the request if authenticated
        response = await call_next(request)
        return response


# Create a global instance
auth_middleware = AuthMiddleware()

# Function to get current user with middleware
def get_current_user_middleware(request: Request) -> dict:
    """
    Dependency function to get current user using middleware
    """
    return auth_middleware.verify_user_middleware(request)