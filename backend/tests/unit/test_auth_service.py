import pytest
from unittest.mock import patch
from src.services.auth_service import AuthService
from src.models.chat import AuthenticationStatus, AuthenticationStatusEnum


def test_verify_password():
    """Test password verification functionality."""
    password = "testpassword"
    hashed = AuthService.get_password_hash(password)

    assert AuthService.verify_password(password, hashed) is True
    assert AuthService.verify_password("wrongpassword", hashed) is False


def test_create_and_verify_token():
    """Test JWT token creation and verification."""
    data = {"sub": "testuser", "role": "user"}
    token = AuthService.create_access_token(data)

    token_data = AuthService.verify_token(token)
    assert token_data is not None
    assert token_data.username == "testuser"


def test_get_authentication_status_with_valid_token():
    """Test getting authentication status with a valid token."""
    # Create a valid token
    token_data = {"sub": "testuser"}
    token = AuthService.create_access_token(token_data)

    # Get authentication status
    auth_status = AuthService.get_authentication_status(token)

    assert auth_status.status == AuthenticationStatusEnum.authenticated
    assert auth_status.user_id == "testuser"


def test_get_authentication_status_with_invalid_token():
    """Test getting authentication status with an invalid token."""
    auth_status = AuthService.get_authentication_status("invalid_token")

    assert auth_status.status == AuthenticationStatusEnum.unauthenticated
    assert auth_status.user_id is None


def test_get_authentication_status_with_no_token():
    """Test getting authentication status with no token."""
    auth_status = AuthService.get_authentication_status(None)

    assert auth_status.status == AuthenticationStatusEnum.unauthenticated
    assert auth_status.user_id is None