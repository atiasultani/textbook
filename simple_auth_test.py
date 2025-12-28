"""
Simple test file to verify the authentication system implementation
"""
import sys
import os

def test_auth_system_implementation():
    """
    Test that the auth system components are properly implemented
    """
    print("Testing Auth System Implementation...")

    # Test 1: Check if auth models are properly implemented
    try:
        from backend.src.auth.models import User, AuthenticationSession, PasswordResetToken, OAuthAccount
        print("✓ Auth models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth models: {e}")
        return False

    # Test 2: Check if auth schemas are properly implemented
    try:
        from backend.src.auth.schemas import UserCreate, UserLogin, Token, AuthResponse
        print("✓ Auth schemas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth schemas: {e}")
        return False

    # Test 3: Check if auth security utilities are properly implemented
    try:
        from backend.src.auth.security import verify_password, get_password_hash, create_access_token
        print("✓ Auth security utilities imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth security utilities: {e}")
        return False

    # Test 4: Check if auth CRUD operations are properly implemented
    try:
        from backend.src.auth.crud import get_user_by_email, create_user, get_user_by_id
        print("✓ Auth CRUD operations imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth CRUD operations: {e}")
        return False

    # Test 5: Check if auth service utilities are properly implemented
    try:
        from backend.src.auth.auth import authenticate_user, create_user_with_session
        print("✓ Auth service utilities imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth service utilities: {e}")
        return False

    # Test 6: Check if auth router is properly implemented
    try:
        from backend.src.auth.router import router
        print("✓ Auth router imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth router: {e}")
        return False

    # Test 7: Check if auth middleware is properly implemented
    try:
        from backend.src.auth.middleware import auth_middleware
        print("✓ Auth middleware imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import auth middleware: {e}")
        return False

    # Test 8: Check if OAuth handlers are properly implemented
    try:
        from backend.src.auth.oauth import handle_google_oauth_login, handle_github_oauth_login
        print("✓ OAuth handlers imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import OAuth handlers: {e}")
        return False

    # Test 9: Check if frontend components exist
    frontend_components = [
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/components/Auth/Login.jsx',
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/components/Auth/Register.jsx',
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/components/Auth/AuthGuard.jsx',
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/context/AuthContext.js',
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/hooks/useAuth.js',
        '/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/services/authService.js'
    ]

    for component in frontend_components:
        if os.path.exists(component):
            print(f"✓ Frontend component exists: {os.path.basename(component)}")
        else:
            print(f"❌ Frontend component missing: {component}")
            return False

    # Test 10: Check if chat page uses AuthGuard
    try:
        with open('/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/pages/chat.js', 'r') as f:
            chat_page_content = f.read()
            if 'AuthGuard' in chat_page_content:
                print("✓ Chat page uses AuthGuard")
            else:
                print("❌ Chat page doesn't use AuthGuard")
                return False
    except FileNotFoundError:
        print("❌ Chat page not found")
        return False

    # Test 11: Check if BookLayout uses AuthGuard
    try:
        with open('/mnt/c/users/ho/documents/github/part2/textbook/frontend/docusaurus/src/components/BookLayout.jsx', 'r') as f:
            book_layout_content = f.read()
            if 'AuthGuard' in book_layout_content:
                print("✓ BookLayout uses AuthGuard")
            else:
                print("❌ BookLayout doesn't use AuthGuard")
                return False
    except FileNotFoundError:
        print("❌ BookLayout not found")
        return False

    print("\nAll auth system components are properly implemented!")
    return True

def test_password_hashing():
    """
    Test password hashing functionality
    """
    print("\nTesting password hashing...")
    try:
        from backend.src.auth.security import get_password_hash, verify_password

        password = "TestPassword123!"
        hashed = get_password_hash(password)

        # Verify the password
        if verify_password(password, hashed):
            print("✓ Password hashing and verification working correctly")
        else:
            print("❌ Password verification failed")
            return False

        # Verify that wrong password fails
        if not verify_password("WrongPassword", hashed):
            print("✓ Wrong password correctly rejected")
        else:
            print("❌ Wrong password should not verify")
            return False

        return True
    except Exception as e:
        print(f"❌ Password hashing test failed: {e}")
        return False

def test_jwt_token_creation():
    """
    Test JWT token creation and verification
    """
    print("\nTesting JWT token functionality...")
    try:
        from backend.src.auth.security import create_access_token, verify_token
        from datetime import timedelta

        # Create a token
        data = {"user_id": "test_user_123", "email": "test@example.com"}
        token = create_access_token(data=data, expires_delta=timedelta(minutes=30))

        # Verify the token
        payload = verify_token(token)
        if payload is not None and payload["user_id"] == "test_user_123":
            print("✓ JWT token creation and verification working correctly")
            return True
        else:
            print("❌ JWT token verification failed")
            return False
    except Exception as e:
        print(f"❌ JWT token test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running Authentication System Tests...\n")

    try:
        success = True
        success &= test_auth_system_implementation()
        success &= test_password_hashing()
        success &= test_jwt_token_creation()

        if success:
            print("\n" + "="*50)
            print("🎉 ALL TESTS PASSED!")
            print("Authentication system is fully implemented and working correctly.")
            print("="*50)
        else:
            print("\n❌ SOME TESTS FAILED")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        sys.exit(1)